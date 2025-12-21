from copy import deepcopy
import logging
from typing import Any
import aiofiles
import json
import requests
from requests.exceptions import HTTPError

from injector import inject
from rabbitmq_admin import AdminAPI
import urllib.parse

from cezzis_com_bootstrapper.domain.config.rabbitmq_options import RabbitMqOptions
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_binding import RabbitMqBinding
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_configuration import RabbitMqConfiguration
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_exchange import RabbitMqExchange
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

    async def create_vhost_if_not_exists(self, vhost: str) -> None:
        """Creates a RabbitMQ virtual host if it does not already exist."""

        existing_vhost: Any | None = None

        try:
            self.logger.info(f"Checking if RabbitMQ vhost '{vhost}' exists", extra={"rabbitmq_vhost": vhost})
            existing_vhost = self.admin_client.get_vhost(name=vhost)
        except HTTPError as e:
            if e.response.status_code == 404:
                self.logger.info(f"RabbitMQ vhost '{vhost}' does not exist", extra={"rabbitmq_vhost": vhost})
                existing_vhost = None
            else:
                raise

        if existing_vhost is None:
            self.logger.info(f"Creating RabbitMQ vhost '{vhost}'", extra={"rabbitmq_vhost": vhost})
            self.admin_client.create_vhost(name=vhost)
        else:
            self.logger.info(f"RabbitMQ vhost '{vhost}' already exists", extra={"rabbitmq_vhost": vhost})

    async def create_user_if_not_exists(self, username: str, password: str, tags: str = "") -> None:
        """Creates a RabbitMQ user if it does not already exist."""
        existing_user: Any | None = None

        try:
            self.logger.info(f"Checking if RabbitMQ user '{username}' exists", extra={"rabbitmq_user": username})
            existing_user = self.admin_client.get_user(name=username)
        except HTTPError as e:
            if e.response.status_code == 404:
                self.logger.info(f"RabbitMQ user '{username}' does not exist", extra={"rabbitmq_user": username})
                existing_user = None
            else:
                raise


        if existing_user is None:
            self.logger.info(f"Creating RabbitMQ user '{username}'", extra={"rabbitmq_user": username})
            self.admin_client.create_user(name=username, password=password, tags=tags)
        else:
            self.logger.info(f"RabbitMQ user '{username}' already exists", extra={"rabbitmq_user": username})

    async def assign_vhost_permissions(self, vhost: str, username: str, configure: str = ".*", write: str = ".*", read: str = ".*") -> None:
        """Assigns permissions to a user for a specific virtual host."""
        self.logger.info(f"Assigning permissions for user '{username}' on vhost '{vhost}'", extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost})
        
        existing_user_permissions: Any | None = None

        try:
            self.logger.info(f"Checking for existing permissions for user '{username}' on vhost '{vhost}'", extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost})
            existing_user_permissions = self.admin_client.get_user_permission(name=username, vhost=vhost)
        except HTTPError as e:
            if e.response.status_code == 404:
                self.logger.info(f"Permissions for user '{username}' on vhost '{vhost}' do not exist", extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost})
                existing_user_permissions = None
            else:
                raise


        if existing_user_permissions is not None:
            self.logger.info(f"Existing user permissions found for user '{username}' on vhost '{vhost}'", extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost})

            if (existing_user_permissions.get("configure") == configure and
                existing_user_permissions.get("write") == write and
                existing_user_permissions.get("read") == read):
                self.logger.info(f"User '{username}' already has the required permissions on vhost '{vhost}'", extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost})
                return
            
            self.logger.info(f"Deleting existing permissions for user '{username}' on vhost '{vhost}'", extra={"rabbitmq_user": username, "rabbitmq_vhost": vhost})
            self.admin_client.delete_user_permission(name=username, vhost=vhost)

        self.admin_client.create_user_permission(name=username, vhost=vhost, configure=configure, write=write, read=read)

    async def list_vhost_users(self, vhost: str) -> list[str]:
        """Lists all RabbitMQ users for a specific virtual host."""
        existing_users = self.admin_client.list_users()

        vhost_users: list[str] = []

        for user in existing_users:
            if user["name"] != self.rabbitmq_options.admin_username:
                user_permissions = self.admin_client.list_user_permissions(name=user["name"])
                for perm in user_permissions:
                    if perm["vhost"] == vhost:
                        vhost_users.append(user["name"])
                        break

        return vhost_users

    async def delete_user_from_vhost(self, vhost: str, username: str) -> None:
        """Deletes a RabbitMQ user from a specific virtual host."""
        self.admin_client.delete_user(name=username)

    async def list_exchanges_in_vhost(self, vhost: str) -> list[str]:
        """Lists all exchanges in a specific virtual host, excluding those starting with 'amq.' and empty names."""
        exchanges = self.admin_client.list_exchanges_for_vhost(vhost=vhost)
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
                self.logger.info(f"Exchange '{exchange_def.name}' already exists in vhost '{vhost}'", extra={"rabbitmq_exchange": exchange_def.name, "rabbitmq_vhost": vhost})
                return

        self.logger.info(f"Creating exchange '{exchange_def.name}' in vhost '{vhost}'", extra={"rabbitmq_exchange": exchange_def.name, "rabbitmq_vhost": vhost})
        self.admin_client.create_exchange_for_vhost(
            exchange=exchange_def.name,
            vhost=vhost,
            body={
                "type": exchange_def.type,
                "durable": exchange_def.durable,
                "auto_delete": exchange_def.auto_delete,
                "internal": exchange_def.internal,
            }
        )

    async def delete_exchange_from_vhost(self, vhost: str, exchange_name: str) -> None:
        """Deletes an exchange from a specific virtual host."""
        self.logger.info(f"Deleting exchange '{exchange_name}' from vhost '{vhost}'", extra={"rabbitmq_exchange": exchange_name, "rabbitmq_vhost": vhost})
        self.admin_client.delete_exchange_for_vhost(
            exchange=exchange_name,
            vhost=vhost,
        )

    async def list_queues_in_vhost(self, vhost: str) -> list[str]:
        """Lists all exchanges in a specific virtual host."""

        queues = self._get('/api/queues/{0}'.format(
            urllib.parse.quote_plus(vhost)
        ))

        return [queue["name"] for queue in queues]

    async def create_queue_for_vhost(self, vhost: str, queue_def: RabbitMqQueue) -> None:
        """Creates a queue in a specific virtual host."""
        self.logger.info(f"Creating queue '{queue_def.name}' in vhost '{vhost}'", extra={"rabbitmq_queue": queue_def.name, "rabbitmq_vhost": vhost})
        self._put(
            path='/api/queues/{0}/{1}'.format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(queue_def.name)
            ),
            data={
                "durable": queue_def.durable,
                "auto_delete": queue_def.auto_delete,
                "exclusive": queue_def.exclusive,
                "arguments": queue_def.arguments,
            }
        )

    async def create_queue_if_not_exists(self, vhost: str, queue_def: RabbitMqQueue) -> None:
        """Creates a queue in a specific virtual host if it does not already exist."""
        existing_queues = await self.list_queues_in_vhost(vhost=vhost)

        for queue in existing_queues:
            if queue == queue_def.name:
                self.logger.info(f"Queue '{queue_def.name}' already exists in vhost '{vhost}'", extra={"rabbitmq_queue": queue_def.name, "rabbitmq_vhost": vhost})
                return

        self.logger.info(f"Creating queue '{queue_def.name}' in vhost '{vhost}'", extra={"rabbitmq_queue": queue_def.name, "rabbitmq_vhost": vhost})
        
        await self.create_queue_for_vhost(
            vhost=vhost,
            queue_def=queue_def
        )

    async def delete_queue_for_vhost(self, vhost: str, queue_name: str) -> None:
        """Deletes a queue from a specific virtual host."""
        self.logger.info(f"Deleting queue '{queue_name}' from vhost '{vhost}'", extra={"rabbitmq_queue": queue_name, "rabbitmq_vhost": vhost})
        self._delete(
            path='/api/queues/{0}/{1}'.format(
                urllib.parse.quote_plus(vhost),
                urllib.parse.quote_plus(queue_name)
            )
        )

    async def LoadFromFileAsync(self, file_path: str) -> RabbitMqConfiguration:
        """Loads RabbitMQ configuration from a JSON file."""

        self.logger.info(f"Loading RabbitMQ configuration from {file_path}")

        async with aiofiles.open(file_path, mode='r') as file:
            logger = logging.getLogger("rabbitmq_configuration_loader")
            content = await file.read()
            data = json.loads(content)

            rabbitmq_configuration = RabbitMqConfiguration(
                exchanges=[RabbitMqExchange(**ex) for ex in data.get("exchanges", [])],
                queues=[RabbitMqQueue(**q) for q in data.get("queues", [])],
                bindings=[RabbitMqBinding(**b) for b in data.get("bindings", [])],
            )
            logger.info(f"Loaded RabbitMQ configuration from {file_path}")
            
            return rabbitmq_configuration
        

    def _get(self, path: str):
        """
        A wrapper for getting things from the RabbitMQ Management HTTP API.
        """
        kwargs = {'url': self.admin_client.url + path}
        kwargs['auth'] = self.admin_client.auth

        headers = deepcopy(self.admin_client.headers)
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers

        response = requests.get(**kwargs)
        response.raise_for_status()

        return response.json()
    
    def _put(self, path: str, data: dict):
        """
        A wrapper for putting things to the RabbitMQ Management HTTP API.
        """
        kwargs = {'url': self.admin_client.url + path}
        kwargs['auth'] = self.admin_client.auth

        headers = deepcopy(self.admin_client.headers)
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers

        kwargs['data'] = json.dumps(data)

        response = requests.put(**kwargs)
        response.raise_for_status()

    def _delete(self, path: str):
        """
        A wrapper for deleting things from the RabbitMQ Management HTTP API.
        """
        kwargs = {'url': self.admin_client.url + path}
        kwargs['auth'] = self.admin_client.auth

        headers = deepcopy(self.admin_client.headers)
        headers.update(kwargs.get('headers', {}))
        kwargs['headers'] = headers

        response = requests.delete(**kwargs)
        response.raise_for_status()