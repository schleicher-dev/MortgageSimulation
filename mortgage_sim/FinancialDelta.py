import typing as ty


class FinancialDelta(object):
    def __init__(self, months: ty.Optional[int] = None, years: ty.Optional[int] = None) -> None:
        self._months: ty.Optional[int] = months if months else 0 + (years * 12 if years else 0)

    @property
    def months(self):
        return self._months

    @staticmethod
    def _get_months(other: ty.Union['FinancialDelta', int]) -> int:
        if isinstance(other, int):
            return other
        return other._months

    def __add__(self, other: ty.Union['FinancialDelta', int]) -> 'FinancialDelta':
        return __class__(months=self._months + self._get_months(other))

    def __lt__(self, other: ty.Union['FinancialDelta', int]) -> bool:
        return self._months < self._get_months(other)

    def __le__(self, other: ty.Union['FinancialDelta', int]) -> bool:
        return self._months <= self._get_months(other)

    def __gt__(self, other: ty.Union['FinancialDelta', int]) -> bool:
        return self._get_months(other) < self._months

    def __ge__(self, other: ty.Union['FinancialDelta', int]) -> bool:
        return self._get_months(other) <= self._months

    def __eq__(self, other: ty.Union['FinancialDelta', int]) -> bool:
        return self._months == self._get_months(other)
    
    def __repr__(self) -> str:
        return f'{self.months}\'\''

