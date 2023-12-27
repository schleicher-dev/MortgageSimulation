from mortgage_sim.FinancialDelta import FinancialDelta

import typing as ty


class FinancialDate(object):
    def __init__(self, year: int, month: int) -> None:
        self._year: int = year
        self._month: int = month
        
    @property
    def year(self) -> int:
        return self._year
        
    @property
    def month(self) -> int:
        return self._month
        
    def __add__(self, other: FinancialDelta) -> 'FinancialDate':
        if not isinstance(other, FinancialDelta):
            raise ValueError(f'Cannot add {other.__class__.__name__} to {__class__.__name__}')
        extra_years, month = divmod(self._month + other.months - 1, 12)
        return FinancialDate(year=self._year + extra_years, month=month +1)

    def __sub__(self, other: 'FinancialDate') -> FinancialDelta:
        if not isinstance(other, FinancialDate):
            raise ValueError(f'Cannot subtract {other.__class__.__name__} to {__class__.__name__}')
        months = self._month - other._month
        months += (self._year - other._year) * 12
        return FinancialDelta(months=months)
    
    def __lt__(self, other: 'FinancialDate') -> bool:
        if not isinstance(other, FinancialDate):
            raise ValueError(f'Cannot compare {other.__class__.__name__} to {__class__.__name__}')
        if self._year == other._year:
            return self._month < other._month
        return self._year < other._year

    def __le__(self, other: 'FinancialDate') -> bool:
        if not isinstance(other, FinancialDate):
            raise ValueError(f'Cannot compare {other.__class__.__name__} to {__class__.__name__}')
        if self._year == other._year:
            return self._month <= other._month
        return self._year <= other._year

    def __gt__(self, other: 'FinancialDate') -> bool:
        if not isinstance(other, FinancialDate):
            raise ValueError(f'Cannot compare {other.__class__.__name__} to {__class__.__name__}')
        if self._year == other._year:
            return other._month < self._month
        return other._year < self._year

    def __ge__(self, other: 'FinancialDate') -> bool:
        if not isinstance(other, FinancialDate):
            raise ValueError(f'Cannot compare {other.__class__.__name__} to {__class__.__name__}')
        if self._year == other._year:
            return other._month <= self._month
        return other._year <= self._year

    def __eq__(self, other: 'FinancialDate') -> bool:
        if not isinstance(other, FinancialDate):
            raise ValueError(f'Cannot compare {other.__class__.__name__} to {__class__.__name__}')
        return self._year == other._year and self._month == other._month
    
    def __repr__(self) -> str:
        return f'{self.year:02d}\'{self.month:02d}\'\''