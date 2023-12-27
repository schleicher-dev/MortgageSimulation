from mortgage_sim.FinancialDate import FinancialDate
from mortgage_sim.Mortgage import Mortgage
from mortgage_sim.PaybackStrategy import PaybackStrategy

import random
import typing as ty


class RandomPaybackStrategy(PaybackStrategy):
    def _unscheduled_payments_order(self, mortgages: ty.List[Mortgage]) -> ty.List[Mortgage]:
        return sorted(mortgages, key=lambda _: (random.randint(0, len(mortgages)), random.randint(0, len(mortgages))))