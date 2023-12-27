from decimal import Decimal
import typing as ty
from mortgage_sim.FinancialDate import FinancialDate
from mortgage_sim.FinancialDelta import FinancialDelta
from mortgage_sim.FinancialPosition import FinancialPosition

from mortgage_sim.types import Number
from mortgage_sim.TemporalCollection import TemporalCollection


class Wallet(object):
    def __init__(self, amount: ty.Optional[Number] = None) -> None:
        self.current_amount: Decimal = Decimal(amount) if amount else Decimal(0)
        self._saving_policies: TemporalCollection[FinancialPosition] = TemporalCollection[FinancialPosition]()
        
    def __add__(self, other: Number) -> 'Wallet':
        self.current_amount += Decimal(other)
        return self
        
    def __sub__(self, other: Number) -> 'Wallet':
        self.current_amount -= Decimal(other)
        return self
    
    def add_saving_policy(self, name: str, when: FinancialDate, amount: Number, recurrence: ty.Optional[FinancialDelta] = None) -> ty.Self:
        position = FinancialPosition(name, when, amount, recurrence)
        self._saving_policies.set_value(name, when, position)
        return self
    
    def remove_saving_policy(self, name: str, when: FinancialDate) -> ty.Self:
        self._saving_policies.set_value(name, when, None)
        return self
    
    def _get_saving_policy_values(self, when: FinancialDate) -> ty.Generator[Decimal, None, None]:
        for _, value in self._saving_policies.values(when):
            if value.recurrence is None:
                yield value.amount
                continue
            factor = (when - value.when).months // value.recurrence.months
            yield factor * value.amount
    
    def get_effective_saving_policy_value(self, when: FinancialDate) -> Decimal:
        return round(sum(self._get_saving_policy_values(when)), 2)
    
    def get_surplus(self, when: FinancialDate) -> Decimal:
        surplus = self.current_amount - self.get_effective_saving_policy_value(when)
        return max(0, surplus)
    