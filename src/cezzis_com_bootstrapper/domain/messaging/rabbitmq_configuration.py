from dataclasses import dataclass

from cezzis_com_bootstrapper.domain.messaging.rabbitmq_binding import RabbitMqBinding
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_exchange import RabbitMqExchange
from cezzis_com_bootstrapper.domain.messaging.rabbitmq_queue import RabbitMqQueue


@dataclass
class RabbitMqConfiguration:
    exchanges: list[RabbitMqExchange]
    queues: list[RabbitMqQueue]
    bindings: list[RabbitMqBinding]
