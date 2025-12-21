from enum import Enum


class RabbitMqExchangeType(Enum):
    DIRECT = "direct"
    FANOUT = "fanout"
    TOPIC = "topic"
