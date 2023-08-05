from dataclasses import dataclass, field
from enum import Enum

from core.number.BigFloat import BigFloat


class Status(Enum):
    NEW = 'new'
    SUBMITTED = 'submitted'
    CANCELLED = 'cancelled'
    EXECUTED = 'executed'
    ERROR = 'error'

    @staticmethod
    def parse(value):
        result = [member for name, member in Status.__members__.items() if member.value.lower() == value.lower()]
        return result[0]


@dataclass
class InstrumentTrade:
    instrument_from: str
    instrument_to: str
    quantity: BigFloat
    price: BigFloat = field(default=None)
    value: BigFloat = field(default=None)
    status: Status = field(default=Status.NEW)
    description: str = field(default=None)
    order_id: str = field(default=None)
    interval: int = field(default=None)
