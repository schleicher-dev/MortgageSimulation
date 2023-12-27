from mortgage_sim.FinancialDate import FinancialDate
from mortgage_sim.FinancialDelta import FinancialDelta
from mortgage_sim.types import Number


import typing as ty
from decimal import Decimal


class FinancialPosition(object):
    def __init__(self, name: str, when: FinancialDate, amount: ty.Optional[Number] = None, recurrence: ty.Optional[FinancialDelta] = None) -> None:
        self.name: str = name
        self.when: FinancialDate = when
        self.amount: Decimal = Decimal(amount) if amount else Decimal(0)
        self.recurrence: ty.Optional[FinancialDelta] = recurrence
        
    def __repr__(self) -> str:
        return f'<{__name__} name={self.name} when={self.when} amount={self.amount} recurrence={self.recurrence}>'
