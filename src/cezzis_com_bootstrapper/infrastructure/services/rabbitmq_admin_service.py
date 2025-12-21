import asyncio
import json
import logging
import urllib.parse
from copy import deepcopy
from typing import Any

import aiofiles
import aiohttp
from dacite import Config, from_dict
from injector import inject
from rabbitmq_admin import AdminAPI
from requests.exceptions import HTTPError

from cezzis_com_bootstrapper.domain.config.rabbitmq_options import RabbitMqOptions
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_binding import RabbitMqBinding
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_binding_type import RabbitMqBindingType
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_configuration import RabbitMqConfiguration
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_exchange import RabbitMqExchange
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_exchange_type import RabbitMqExchangeType
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_queue import RabbitMqQueue
from cezzis_com_bootstrapper.infrastructure.services.irabbitmq_admin_service import IRabbitMqAdminService


class RabbitMqAdminService(IRabbitMqAdminService):
    @inject
    def __init__(self, rabbitmq_options: RabbitMqOptions):
        self.rabbitmq_options = rabbitmq_options
        self.logger = logging.getLogger("rabbitmq_admin_service")
        self.admin_client = AdminAPI(
            url=f"{rabbitmq_options.host}:{rabbitmq_options.admin_port}",
            auth=(
                rabbitmq_options.admin_username,
                rabbitmq_options.admin_password,
            ),
        )

    async def load_from_file(self, file_path: str) -> RabbitMqConfiguration:
        """Loads RabbitMQ configuration from a JSON file."""

        self.logger.info(f"Loading RabbitMQ configuration from {file_path}")

        async with aiofiles.open(file_path, mode="r") as file:
            logger = logging.getLogger("rabbitmq_configuration_loader")
            content = await file.read()
            data = json.loads(content)

            rabbitmq_configuration = from_dict(
                data_class=RabbitMqConfiguration,
                data=data,
                config=Config(
                    type_hooks={
                        RabbitMqBindingType: RabbitMqBindingType,
                        RabbitMqExchangeType: RabbitMqExchangeType,
                    }
                ),
            )
            logger.info(f"Loaded RabbitMQ configuration from {file_path}")

            return rabbitmq_configuration

    async def create_vhost_if_not_exists(self, vhost: str) -> None:
        """Creates a RabbitMQ virtual host if it does not already exist."""

        existing_vhost: Any | None = None

        try:
            self.logger.info(f"Checking if RabbitMQ vhost '{vhost}' exists", extra={"rabbitmq_vhost": vhost})
            existing_vhost = await asyncio.to_thread(self.admin_client.get_vhost, name=vhost)
        except HTTPError as e:
            if e.response.status_code == 404:
                self.logger.info(f"RabbitMQ vhost '{vhost}' does not exist", extra={"rabbitmq_vhost": vhost})
                existing_vhost = None
            else:
                raise

        if existing_vhost is None:
            self.logger.info(f"Creating RabbitMQ vhost '{vhost}'", extra={"rabbitmq_vhost": vhost})
            await asyncio.to_thread(self.admin_client.create_vhost, name=vhost)
        else:
            self.logger.info(f"RabbitMQ vhost '{vhost}' already exists", extra={"rabbitmq_vhost": vhost})

    async def create_user_if_not_exists(self, username: str, password: str, tags: str = "") -> None:
        """Creates a RabbitMQ user if it does not already exist."""
        existing_user: Any | None = None

        try:
            self.logger.info(f"Checking if RabbitMQ user '{username}' exists", extra={"rabbitmq_user": username})
            existing_user = await asyncio.to_thread(self.admin_client.get_user, name=username)
        except HTTPError as e:
            if e.response.status_code == 404:
                self.logger.info(f"RabbitMQ user '{username}' does not exist", extra={"rabbitmq_user": username})
                existing_user = None
            else:
                raise

        if existing_user is None:
            self.logger.info(f"Creating RabbitMQ user '{username}'", extra={"rabbitmq_user": username})
            await asyncio.to_thread(self.admin_client.create_user, name=username, password=password, tags=tags)
        else:
            self.logger.info(f"RabbitMQ user '{username}' already exists", extra={"rabbitmq_user": username})

    async def assign_vhost_permissions(
        self, vhost: str, username: str, configure: str = ".*", write: str = ".*", read: str = ".*"
    ) -> None:
        """Assigns permissions to a user for a specific virtual host."""
        self.logger.info(
            f"Assigning permissions for user '{username}' on vhost '{vhost}'",
            extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost},
        )

        existing_user_permissions: Any | None = None

        try:
            self.logger.info(
                f"Checking for existing permissions for user '{username}' on vhost '{vhost}'",
                extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost},
            )
            existing_user_permissions = await asyncio.to_thread(
                self.admin_client.get_user_permission, name=username, vhost=vhost
            )
        except HTTPError as e:
            if e.response.status_code == 404:
                self.logger.info(
                    f"Permissions for user '{username}' on vhost '{vhost}' do not exist",
                    extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost},
                )
                existing_user_permissions = None
            else:
                raise

        if existing_user_permissions is not None:
            self.logger.info(
                f"Existing user permissions found for user '{username}' on vhost '{vhost}'",
                extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost},
            )

            if (
                existing_user_permissions.get("configure") == configure
                and existing_user_permissions.get("write") == write
                and existing_user_permissions.get("read") == read
            ):
                self.logger.info(
                    f"User '{username}' already has the required permissions on vhost '{vhost}'",
                    extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost},
                )
                return

            self.logger.info(
                f"Deleting existing permissions for user '{username}' on vhost '{vhost}'",
                extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost},
            )
            await asyncio.to_thread(self.admin_client.delete_user_permission, name=username, vhost=vhost)

        await asyncio.to_thread(
            self.admin_client.create_user_permission,
            name=username,
            vhost=vhost,
            configure=configure,
            write=write,
            read=read,
        )

    async def list_vhost_users(self, vhost: str) -> list[str]:
        """Lists all RabbitMQ users for a specific virtual host."""
        existing_users = await asyncio.to_thread(self.admin_client.list_users)

        vhost_users: list[str] = []

        for user in existing_users:
            if user["name"] != self.rabbitmq_options.admin_username:
                user_permissions = await asyncio.to_thread(self.admin_client.list_user_permissions, name=user["name"])
                for perm in user_permissions:
                    if perm["vhost"] == vhost:
                        vhost_users.append(user["name"])
                        break

        return vhost_users

    async def delete_user_from_vhost(self, vhost: str, username: str) -> None:
        """Deletes a RabbitMQ user from a specific virtual host."""
        await asyncio.to_thread(self.admin_client.delete_user, name=username)

    async def list_exchanges_in_vhost(self, vhost: str) -> list[str]:
        """Lists all exchanges in a specific virtual host, excluding those starting with 'amq.' and empty names."""
        exchanges = await asyncio.to_thread(self.admin_client.list_exchanges_for_vhost, vhost=vhost)
        filtered = []
        for exchange in exchanges:
            name = exchange.get("name", "")
            if name and not name.startswith("amq."):
                filtered.append(name)

        return filtered

    async def create_exchange_if_not_exists(self, vhost: str, exchange_def: RabbitMqExchange) -> None:
        """Creates an exchange in a specific virtual host if it does not already exist."""
        existing_exchanges = await self.list_exchanges_in_vhost(vhost=vhost)

        for exchange in existing_exchanges:
            if exchange == exchange_def.name:
                self.logger.info(
                    f"Exchange '{exchange_def.name}' already exists in vhost '{vhost}'",
                    extra={"rabbitmq_exchange": exchange_def.name, "rabbitmq_vhost": vhost},
                )
                return

        self.logger.info(
            f"Creating exchange '{exchange_def.name}' in vhost '{vhost}'",
            extra={"rabbitmq_exchange": exchange_def.name, "rabbitmq_vhost": vhost},
        )
        await asyncio.to_thread(
            self.admin_client.create_exchange_for_vhost,
            exchange=exchange_def.name,
            vhost=vhost,
            body={
                "type": exchange_def.type.value,
                "durable": exchange_def.durable,
                "auto_delete": exchange_def.auto_delete,
                "internal": exchange_def.internal,
            },
        )

    async def delete_exchange_from_vhost(self, vhost: str, exchange_name: str) -> None:
        """Deletes an exchange from a specific virtual host."""
        self.logger.info(
            f"Deleting exchange '{exchange_name}' from vhost '{vhost}'",
            extra={"rabbitmq_exchange": exchange_name, "rabbitmq_vhost": vhost},
        )
        await asyncio.to_thread(
            self.admin_client.delete_exchange_for_vhost,
            exchange=exchange_name,
            vhost=vhost,
        )

    async def list_queues_in_vhost(self, vhost: str) -> list[str]:
        """Lists all queues in a specific virtual host."""

        queues = await self._get("/api/queues/{0}".format(urllib.parse.quote_plus(vhost)))

        return [queue["name"] for queue in queues]

    async def create_queue_for_vhost(self, vhost: str, queue_def: RabbitMqQueue) -> None:
        """Creates a queue in a specific virtual host."""
        self.logger.info(
            f"Creating queue '{queue_def.name}' in vhost '{vhost}'",
            extra={"rabbitmq_queue": queue_def.name, "rabbitmq_vhost": vhost},
        )
        await self._put(
            path="/api/queues/{0}/{1}".format(urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(queue_def.name)),
            data={
                "durable": queue_def.durable,
                "auto_delete": queue_def.auto_delete,
                "exclusive": queue_def.exclusive,
                "arguments": queue_def.arguments,
            },
        )

    async def create_queue_if_not_exists(self, vhost: str, queue_def: RabbitMqQueue) -> None:
        """Creates a queue in a specific virtual host if it does not already exist."""
        existing_queues = await self.list_queues_in_vhost(vhost=vhost)

        for queue in existing_queues:
            if queue == queue_def.name:
                self.logger.info(
                    f"Queue '{queue_def.name}' already exists in vhost '{vhost}'",
                    extra={"rabbitmq_queue": queue_def.name, "rabbitmq_vhost": vhost},
                )
                return

        self.logger.info(
            f"Creating queue '{queue_def.name}' in vhost '{vhost}'",
            extra={"rabbitmq_queue": queue_def.name, "rabbitmq_vhost": vhost},
        )

        await self.create_queue_for_vhost(vhost=vhost, queue_def=queue_def)

    async def delete_queue_for_vhost(self, vhost: str, queue_name: str) -> None:
        """Deletes a queue from a specific virtual host."""
        self.logger.info(
            f"Deleting queue '{queue_name}' from vhost '{vhost}'",
            extra={"rabbitmq_queue": queue_name, "rabbitmq_vhost": vhost},
        )
        await self._delete(
            path="/api/queues/{0}/{1}".format(urllib.parse.quote_plus(vhost), urllib.parse.quote_plus(queue_name))
        )

    async def list_bindings_in_vhost(self, vhost: str) -> list[RabbitMqBinding]:
        """Lists all bindings in a specific virtual host."""
        bindings = await self._get("/api/bindings/{0}".format(urllib.parse.quote_plus(vhost)))

        binding_list: list[RabbitMqBinding] = []

        for binding in bindings:
            existing_binding = RabbitMqBinding(
                source=binding.get("source", ""),
                destination=binding.get("destination", ""),
                destination_type=RabbitMqBindingType(binding.get("destination_type", "")),
                routing_key=binding.get("routing_key", ""),
                arguments=binding.get("arguments", {}),
            )

            if (
                not existing_binding.source
                and existing_binding.routing_key == existing_binding.destination
                and existing_binding.destination_type == RabbitMqBindingType.QUEUE
            ):
                # Skip default direct queue bindings
                continue

            if existing_binding.source and existing_binding.destination:
                binding_list.append(existing_binding)

        return binding_list

    async def create_binding_if_not_exists(self, vhost: str, binding_def: RabbitMqBinding) -> None:
        """Creates a binding in a specific virtual host if it does not already exist."""

        if binding_def.destination_type not in [RabbitMqBindingType.QUEUE, RabbitMqBindingType.EXCHANGE]:
            raise ValueError(f"Invalid destination_type '{binding_def.destination_type}' for binding.")

        existing_bindings = await self.list_bindings_in_vhost(vhost=vhost)

        for binding in existing_bindings:
            if (
                binding.source == binding_def.source
                and binding.destination == binding_def.destination
                and binding.destination_type == binding_def.destination_type
                and binding.routing_key == binding_def.routing_key
            ):
                self.logger.info(
                    f"Binding from '{binding_def.source}' to '{binding_def.destination}' already exists in vhost '{vhost}'",
                    extra={
                        "rabbitmq_vhost": vhost,
                        "rabbitmq_exchange": binding_def.source,
                        "rabbitmq_routing_key": binding_def.routing_key,
                        "rabbitmq_destination": binding_def.destination,
                    },
                )
                return

        self.logger.info(
            f"Creating binding from '{binding_def.source}' to '{binding_def.destination}' in vhost '{vhost}'",
            extra={
                "rabbitmq_vhost": vhost,
                "rabbitmq_exchange": binding_def.source,
                "rabbitmq_routing_key": binding_def.routing_key,
                "rabbitmq_destination": binding_def.destination,
            },
        )

        await self._post(
            path="/api/bindings/{0}/e/{1}/{2}/{3}".format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(binding_def.source),
                binding_def.destination_type.value[0],
                urllib.parse.quote_plus(binding_def.destination),
            ),
            data={
                "routing_key": binding_def.routing_key,
                "arguments": binding_def.arguments,
            },
        )

    async def delete_binding_from_vhost(self, vhost: str, binding_def: RabbitMqBinding) -> None:
        """Deletes a binding from a specific virtual host."""
        self.logger.info(
            f"Deleting binding from '{binding_def.source}' to '{binding_def.destination}' in vhost '{vhost}'",
            extra={
                "rabbitmq_vhost": vhost,
                "rabbitmq_exchange": binding_def.source,
                "rabbitmq_routing_key": binding_def.routing_key,
                "rabbitmq_destination": binding_def.destination,
            },
        )

        bindings = await self._get(
            "/api/bindings/{0}/e/{1}/{2}/{3}".format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(binding_def.source),
                binding_def.destination_type.value[0],
                urllib.parse.quote_plus(binding_def.destination),
            )
        )

        for binding in bindings:
            if binding.get("routing_key", "") == binding_def.routing_key:
                await self._delete(
                    path="/api/bindings/{0}/e/{1}/{2}/{3}/{4}".format(
                        urllib.parse.quote_plus(vhost),
                        urllib.parse.quote_plus(binding_def.source),
                        binding_def.destination_type.value[0],
                        urllib.parse.quote_plus(binding_def.destination),
                        str(binding.get("properties_key", "")),
                    )
                )
                return

    async def _get(self, path: str):
        """
        A wrapper for getting things from the RabbitMQ Management HTTP API using aiohttp.
        """
        url = self.admin_client.url + path
        auth = aiohttp.BasicAuth(*self.admin_client.auth)
        headers = deepcopy(self.admin_client.headers)

        async with aiohttp.ClientSession(auth=auth, headers=headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()

    async def _put(self, path: str, data: dict):
        """
        A wrapper for upserting things from the RabbitMQ Management HTTP API using aiohttp.
        """
        url = self.admin_client.url + path
        auth = aiohttp.BasicAuth(*self.admin_client.auth)
        headers = deepcopy(self.admin_client.headers)

        async with aiohttp.ClientSession(auth=auth, headers=headers) as session:
            async with session.put(url, json=data) as response:
                response.raise_for_status()

    async def _post(self, path: str, data: dict):
        """
        A wrapper for creating things from the RabbitMQ Management HTTP API using aiohttp.
        """
        url = self.admin_client.url + path
        auth = aiohttp.BasicAuth(*self.admin_client.auth)
        headers = deepcopy(self.admin_client.headers)

        async with aiohttp.ClientSession(auth=auth, headers=headers) as session:
            async with session.post(url, json=data) as response:
                response.raise_for_status()

    async def _delete(self, path: str):
        """
        A wrapper for deleting things from the RabbitMQ Management HTTP API using aiohttp.
        """
        url = self.admin_client.url + path
        auth = aiohttp.BasicAuth(*self.admin_client.auth)
        headers = deepcopy(self.admin_client.headers)

        async with aiohttp.ClientSession(auth=auth, headers=headers) as session:
            async with session.delete(url) as response:
                response.raise_for_status()
