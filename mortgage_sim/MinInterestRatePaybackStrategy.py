from mortgage_sim.Mortgage import Mortgage
from mortgage_sim.PaybackStrategy import PaybackStrategy


from typing import List


class MinInterestRatePaybackStrategy(PaybackStrategy):
    def _unscheduled_payments_order(self, mortgages: List[Mortgage]) -> List[Mortgage]:
        return sorted(mortgages, key=lambda m: m.interest_value, reverse=True)
