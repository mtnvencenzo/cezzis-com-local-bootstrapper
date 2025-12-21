from enum import Enum

class RabbitMqBindingType(Enum):
    QUEUE = "queue"
    EXCHANGE = "exchange"