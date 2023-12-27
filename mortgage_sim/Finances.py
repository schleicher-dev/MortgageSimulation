from decimal import Decimal
import typing as ty
from mortgage_sim.FinancialDate import FinancialDate
from mortgage_sim.FinancialDelta import FinancialDelta

from mortgage_sim.TemporalCollection import TemporalCollection
from mortgage_sim.types import Number
from mortgage_sim.FinancialPosition import FinancialPosition


class Finances(object):
    def __init__(self, current_wallet: Number) -> None:
        self.current_wallet: Decimal = Decimal(current_wallet)
        self._incomes: TemporalCollection[FinancialPosition] = TemporalCollection[FinancialPosition]()
        self._expenses: TemporalCollection[FinancialPosition] = TemporalCollection[FinancialPosition]()
    
    def add_income(self, name: str, when: FinancialDate, amount: Number, recurrence: ty.Optional[FinancialDelta] = None) -> 'Finances':
        position = FinancialPosition(name, when, amount, recurrence)
        self._incomes.set_value(name, when, position)
        return self
    
    def remove_income(self, name: str, when: FinancialDate) -> 'Finances':
        self._incomes.set_value(name, when, None)
        return self
    
    def add_expense(self, name: str, when: FinancialDate, amount: Number, recurrence: ty.Optional[FinancialDelta] = None) -> 'Finances':
        position = FinancialPosition(name, when, amount, recurrence)
        self._expenses.set_value(name, when, position)
        return self
    
    def remove_expense(self, name: str, when: FinancialDate) -> 'Finances':
        self._expenses.set_value(name, when, None)
        return self
    
    @staticmethod
    def _is_last_month_entry(entry: FinancialPosition, when: FinancialDate):
        return entry.when <= when < entry.when + FinancialDelta(months=1)
    
    @staticmethod
    def _is_current_entry(entry: FinancialPosition, when: FinancialDate):
        delta = entry.when - when
        if entry.recurrence.months == 0:
            return False
        return entry.when <= when and delta.months % entry.recurrence.months == 0
        
    @classmethod
    def _is_valid_entry(cls, entry: FinancialPosition, when: FinancialDate):
        if entry.recurrence is None:
            return cls._is_last_month_entry(entry, when)
        return cls._is_current_entry(entry, when)
        
    def get_effective_incomes(self, when: FinancialDate) -> ty.Dict[str, Decimal]:
        return [entry for _, entry in self._incomes.values(when) if entry is not None and self._is_valid_entry(entry, when)]
    
    def get_effective_expenses(self, when: FinancialDate) -> ty.Dict[str, Decimal]:
        return [entry for _, entry in self._expenses.values(when) if self._is_valid_entry(entry, when)]
    
    def get_effective_income_value(self, when: FinancialDate) -> Decimal:
        return round(sum(income.amount for income in self.get_effective_incomes(when)), 2)
    
    def get_effective_expense_value(self, when: FinancialDate) -> Decimal:
        return round(sum(expense.amount for expense in self.get_effective_expenses(when)), 2)
    
    def get_effective_balance(self, when: FinancialDate) -> Decimal:
        total_income = self.get_effective_income_value(when)
        total_expense = self.get_effective_expense_value(when)
        return round(total_income - total_expense, 2)

