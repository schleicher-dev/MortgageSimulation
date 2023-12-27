from mortgage_sim.types import Number, Percentage, as_decimal


from decimal import Decimal


class RepaymentParameterSet(object):    
    def __init__(self, min_value: Number | Percentage, max_value: Number | Percentage, payments_per_year: int) -> None:
        self._min_value: Number | Percentage = min_value
        self._max_value: Number | Percentage = max_value
        self._payments_per_year: int = payments_per_year

    def min_value(self, amount: Decimal) -> Decimal:
        return round(self._min_value if isinstance(self._min_value, Number) else as_decimal(self._min_value) * amount, 2)

    def max_value(self, amount: Decimal) -> Decimal:
        return round(self._max_value if isinstance(self._max_value, Number) else as_decimal(self._max_value) * amount, 2)

    @property
    def payments_per_year(self) -> int:
        return self._payments_per_year