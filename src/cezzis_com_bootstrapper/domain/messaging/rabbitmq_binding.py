import dataclasses
from dataclasses import dataclass

from cezzis_com_bootstrapper.domain.messaging.rabbitmq_binding_type import RabbitMqBindingType

@dataclass
class RabbitMqBinding:
    source: str
    destination: str
    destination_type: RabbitMqBindingType = RabbitMqBindingType.QUEUE
    binding_key: str = ""
    arguments: dict = dataclasses.field(default_factory=dict)