from decimal import Decimal
import typing as ty

Number = ty.Union[Decimal, float, int]


class Percentage(object):
    def __init__(self, value: Number) -> None:
        self._value: Decimal = Decimal(value)

    @property
    def decimal_fraction(self):
        return self._value / Decimal(100)

    @property
    def percentage(self):
        return self._value
    
    def __lt__(self, other: 'Percentage') -> bool:
        return self._value < other._value
    
    def __le__(self, other: 'Percentage') -> bool:
        return self._value <= other._value
    
    def __gt__(self, other: 'Percentage') -> bool:
        return self._value > other._value
    
    def __ge__(self, other: 'Percentage') -> bool:
        return self._value >= other._value
    
    def __eq__(self, other: 'Percentage') -> bool:
        return self._value == other._value
    
    def __ne__(self, other: 'Percentage') -> bool:
        return self._value != other._value
    
    def __repr__(self) -> str:
        return f'<Percentage value={self._value}%>'


def as_decimal(value: ty.Union[Percentage, Number]):
    if isinstance(value, Percentage):
        return value.decimal_fraction
    return Decimal(value)
