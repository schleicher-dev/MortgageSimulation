from mortgage_sim.FinancialDate import FinancialDate
from mortgage_sim.Mortgage import Mortgage
from mortgage_sim.PaybackStrategy import PaybackStrategy


import typing as ty


class MinRestDurationPaybackStrategy(PaybackStrategy):
    def _unscheduled_payments_order(self, mortgages: ty.List[Mortgage]) -> ty.List[Mortgage]:
        return sorted(mortgages, key=lambda m: (m.valid_until or FinancialDate(year=9999, month=12), m.interest_value))


