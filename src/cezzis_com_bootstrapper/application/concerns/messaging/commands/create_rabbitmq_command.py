import logging

from injector import inject
from mediatr import GenericQuery, Mediator

from cezzis_com_bootstrapper.domain.config.rabbitmq_options import RabbitMqOptions
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_configuration import RabbitMqConfiguration
from cezzis_com_bootstrapper.infrastructure.services.irabbitmq_admin_service import IRabbitMqAdminService


class CreateRabbitMqCommand(GenericQuery[bool]):
    """Command to initialize RabbitMQ and all infrastructure dependencies."""

    pass


@Mediator.handler
class CreateRabbitMqCommandHandler:
    """Command handler for the CreateRabbitMqCommand."""

    @inject
    def __init__(self, rabbitmq_admin_service: IRabbitMqAdminService, rabbitmq_options: RabbitMqOptions):
        self.rabbitmq_admin_service = rabbitmq_admin_service
        self.rabbitmq_options = rabbitmq_options
        self.logger = logging.getLogger("create_rabbitmq_command_handler")

    async def handle(self, request: CreateRabbitMqCommand) -> bool:
        # --------------------------------------------------------
        # Load the configuration if it exists, otherwise use an empty configuration
        # --------------------------------------------------------
        rabbitmq_configuration = (
            await self.rabbitmq_admin_service.load_from_file(self.rabbitmq_options.app_config_file_path)
            if self.rabbitmq_options.app_config_file_path
            else RabbitMqConfiguration(queues=[], exchanges=[], bindings=[])
        )

        # --------------------------------------------------------
        # Create the vhost
        # --------------------------------------------------------
        await self.rabbitmq_admin_service.create_vhost_if_not_exists(self.rabbitmq_options.vhost)

        # --------------------------------------------------------
        # Create the application user and assign permissions
        # Removing existing users not matching the application user
        # --------------------------------------------------------
        await self.rabbitmq_admin_service.create_user_if_not_exists(
            username=self.rabbitmq_options.app_username,
            password=self.rabbitmq_options.app_password,
        )
        await self.rabbitmq_admin_service.assign_vhost_permissions(
            vhost=self.rabbitmq_options.vhost,
            username=self.rabbitmq_options.app_username,
            configure=".*",
            write=".*",
            read=".*",
        )

        vhost_users = await self.rabbitmq_admin_service.list_vhost_users(self.rabbitmq_options.vhost)
        for user in vhost_users:
            if user != self.rabbitmq_options.app_username:
                self.logger.info(f"Deleting extraneous user '{user}' from vhost '{self.rabbitmq_options.vhost}'")
                await self.rabbitmq_admin_service.delete_user(username=user)

        # --------------------------------------------------------
        # Create exchanges and remove any not in the configuration
        # --------------------------------------------------------
        for exchange_def in rabbitmq_configuration.exchanges:
            await self.rabbitmq_admin_service.create_exchange_if_not_exists(
                vhost=self.rabbitmq_options.vhost,
                exchange_def=exchange_def,
            )

        all_exchanges = await self.rabbitmq_admin_service.list_exchanges_in_vhost(self.rabbitmq_options.vhost)
        for exchange in all_exchanges:
            if exchange not in [ex.name for ex in rabbitmq_configuration.exchanges]:
                await self.rabbitmq_admin_service.delete_exchange_from_vhost(
                    vhost=self.rabbitmq_options.vhost,
                    exchange_name=exchange,
                )

        # --------------------------------------------------------
        # Create queues and remove any not in the configuration
        # --------------------------------------------------------
        for queue_def in rabbitmq_configuration.queues:
            await self.rabbitmq_admin_service.create_queue_if_not_exists(
                vhost=self.rabbitmq_options.vhost,
                queue_def=queue_def,
            )

        all_queues = await self.rabbitmq_admin_service.list_queues_in_vhost(self.rabbitmq_options.vhost)
        for queue in all_queues:
            if queue not in [q.name for q in rabbitmq_configuration.queues]:
                await self.rabbitmq_admin_service.delete_queue_for_vhost(
                    vhost=self.rabbitmq_options.vhost,
                    queue_name=queue,
                )

        # --------------------------------------------------------
        # Create bindings and remove any not in the configuration
        # --------------------------------------------------------
        for binding_def in rabbitmq_configuration.bindings:
            await self.rabbitmq_admin_service.create_binding_if_not_exists(
                vhost=self.rabbitmq_options.vhost,
                binding_def=binding_def,
            )

        all_bindings = await self.rabbitmq_admin_service.list_bindings_in_vhost(self.rabbitmq_options.vhost)
        for binding in all_bindings:
            if binding not in rabbitmq_configuration.bindings:
                await self.rabbitmq_admin_service.delete_binding_from_vhost(
                    vhost=self.rabbitmq_options.vhost,
                    binding_def=binding,
                )

        return True
