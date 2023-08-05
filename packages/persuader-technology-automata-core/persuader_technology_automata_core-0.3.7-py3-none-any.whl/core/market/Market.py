from enum import Enum


class Market(Enum):
    BINANCE = 'binance'

    @staticmethod
    def parse(value):
        result = [member for name, member in Market.__members__.items() if member.value.lower() == value.lower()]
        return result[0]
