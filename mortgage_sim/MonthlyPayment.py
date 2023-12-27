from decimal import Decimal


class MonthlyPayment(object):
    def __init__(self, amount: Decimal, interest_value: Decimal, payback_value: Decimal) -> None:
        self._amount: Decimal = amount
        self._interest_value: Decimal = interest_value
        self._payback_value: Decimal = payback_value
        
    @property
    def amount(self) -> Decimal:
        return self._amount
    
    @property
    def interest_value(self) -> Decimal:
        return self._interest_value
    
    @property
    def payback_value(self) -> Decimal:
        return self._payback_value
    