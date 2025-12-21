import dataclasses
from dataclasses import dataclass

from cezzis_com_bootstrapper.domain.messaging.rabbitmq_exchange_type import RabbitMqExchangeType

@dataclass
class RabbitMqExchange:
    name: str
    type: RabbitMqExchangeType = RabbitMqExchangeType.TOPIC
    durable: bool = True
    auto_delete: bool = False
    internal: bool = False
    arguments: dict = dataclasses.field(default_factory=dict)
