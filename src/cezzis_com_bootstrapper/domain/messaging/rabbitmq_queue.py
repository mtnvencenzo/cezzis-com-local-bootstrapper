import dataclasses
from dataclasses import dataclass

@dataclass
class RabbitMqQueue:
    name: str
    durable: bool = True
    exclusive: bool = False
    auto_delete: bool = False
    arguments: dict = dataclasses.field(default_factory=dict)