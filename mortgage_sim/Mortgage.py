from mortgage_sim.MonthlyPayment import MonthlyPayment
from mortgage_sim.FinancialDate import FinancialDate
from mortgage_sim.PaymentPlan import PaymentPlan
from mortgage_sim.RepaymentParameterSet import RepaymentParameterSet
from mortgage_sim.TemporalValue import TemporalValue
from mortgage_sim.Wallet import Wallet
from mortgage_sim.types import Number, Percentage, as_decimal


import typing as ty
from decimal import Decimal


class Mortgage(object):
    def __init__(self, name: str, initial_amount: Number, interest_rate: Percentage, payback_rate: Percentage,
                 valid_from: ty.Optional[FinancialDate] = None, valid_until: ty.Optional[FinancialDate] = None,
                 repayment_parameter_set: ty.Optional[RepaymentParameterSet] = None) -> None:
        self.name: str = name
        self._initial_amount: Decimal = as_decimal(initial_amount)
        self._current_amount: Decimal = self._initial_amount
        self._interest_rate: TemporalValue[Percentage] = TemporalValue[Percentage](interest_rate)
        self._payback_rate: TemporalValue[ Percentage] = TemporalValue[Percentage](payback_rate)
        self._valid_from: ty.Optional[FinancialDate] = valid_from
        self._valid_until: ty.Optional[FinancialDate] = valid_until
        self._repayment_parameter_set: TemporalValue[RepaymentParameterSet] = TemporalValue[RepaymentParameterSet](repayment_parameter_set)
        self._current_unscheduled_payments_count: int = 0
        self._current_unscheduled_payments_sum: Decimal = Decimal(0)
        self._current_date: ty.Optional[FinancialDate] = None
        self._follow_up_creator: ty.Optional[ty.Callable[['Mortgage', PaymentPlan], 'Mortgage']] = None

    def alter_interest_rate(self, when: FinancialDate, interest_rate: Percentage) -> ty.Self:
        self._interest_rate.set_value(when, interest_rate)
        return self

    def alter_payback_rate(self, when: FinancialDate, payback_rate: Percentage) -> ty.Self:
        self._payback_rate.set_value(when, payback_rate)
        return self
    
    def alter_repayment_parameter_set(self, when: FinancialDate, parameter_set: RepaymentParameterSet) -> ty.Self:
        self._repayment_parameter_set.set_value(when, parameter_set)
        return self
    
    def update_current_date(self, next_date: FinancialDate) -> None:
        if self._current_date is None:
            self._current_date = next_date
            self._current_unscheduled_payments_count = 0
            self._current_unscheduled_payments_sum = Decimal(0)
            return
        
        delta = next_date - self._current_date
        if delta.months != 1:
            raise ValueError(f'next_date must be incremented by 1 month but is incremented by {delta.months}')
        
        if next_date.month == 1:
            self._current_unscheduled_payments_count = 0
            self._current_unscheduled_payments_sum = Decimal(0)
        self._current_date = next_date
        
    def columns(self) -> ty.List[str]:
        return [f'{self.name} Interest', f'{self.name} Payback', f'{self.name} Amount', f'{self.name} Unscheduled']
        
    def execute_payback(self, payment_plan: PaymentPlan, wallet: Wallet) -> None:
        monthly_payment = self.monthly_payment
        self._current_amount += monthly_payment.interest_value
        self._current_amount -= monthly_payment.payback_value
        if self._current_amount < 0.01:
            self._current_amount = Decimal(0)
        
        wallet -= self.monthly_payment.payback_value
        payment_plan.record(f'{self.name} Interest', monthly_payment.interest_value, Decimal(0))
        payment_plan.record(f'{self.name} Payback', monthly_payment.payback_value, Decimal(0))
        payment_plan.record(f'{self.name} Amount', self._current_amount, Decimal(0))
        
    def _execute_unscheduled_payment(self, payment_plan: PaymentPlan, wallet: Wallet, amount: Decimal):
        self._current_amount -= amount
        self._current_unscheduled_payments_sum += amount
        self._current_unscheduled_payments_count += 1
        wallet -= amount
        payment_plan.record(f'{self.name} Unscheduled', amount, Decimal(0))
        
    def execute_unscheduled_payment(self, payment_plan: PaymentPlan, wallet: Wallet) -> None:        
        surplus = wallet.get_surplus(self._current_date)
        payment_plan.record(f'{self.name} Unscheduled', Decimal(0), Decimal(0))
        
        param_set = self.repayment_parameter_set
        if param_set is None:
            return
        
        min_value = param_set.min_value(self.initial_amount)
        max_value = param_set.max_value(self.initial_amount)
        payments_left = max(param_set.payments_per_year - self._current_unscheduled_payments_count, 0)
        if surplus < min_value or max_value <= self._current_unscheduled_payments_sum or payments_left <= 0:
            return
        
        amount_left = min(max_value - self._current_unscheduled_payments_sum, self._current_amount)
        possible_amount = min(surplus, amount_left)
        possible_rest = amount_left - possible_amount
        
        months_left = (FinancialDate(year=self._current_date.year + 1, month=1) - self._current_date).months
        if min_value <= possible_rest or possible_rest == Decimal(0) or months_left == 1 or payments_left == 1:
            self._execute_unscheduled_payment(payment_plan, wallet, possible_amount)
            return
        
        possible_amount -= min_value
        if min_value <= possible_amount:
            self._execute_unscheduled_payment(payment_plan, wallet, possible_amount)
            return      
        
    def register_follow_up_creator(self, follow_up_creator: ty.Callable[['Mortgage'], 'Mortgage']) -> ty.Self:
        self._follow_up_creator = follow_up_creator
        return self
        
    @property
    def current_date(self) -> FinancialDate:
        if self._current_date is None:
            raise ValueError('current_date must be set')
        return self._current_date
        
    @property
    def initial_amount(self) -> Decimal:
        return self._initial_amount
    
    @property
    def current_amount(self) -> Decimal:
        return self._current_amount
        
    @property
    def valid_from(self) -> ty.Optional[FinancialDate]:
        return self._valid_from
        
    @property
    def valid_until(self) -> ty.Optional[FinancialDate]:
        return self._valid_until
    
    @property
    def monthly_payment_amount(self) -> Decimal:
        interest_rate = as_decimal(self._interest_rate.get_value(self.current_date))
        payback_rate = as_decimal(self._payback_rate.get_value(self.current_date))
        return round((interest_rate + payback_rate) * self.initial_amount / Decimal(12), 2)
    
    @property
    def interest_value(self) -> Decimal:
        interest_rate = as_decimal(self._interest_rate.get_value(self.current_date))
        return round(self._current_amount * interest_rate / Decimal(12), 2)
    
    @property
    def payback_value(self) -> Decimal:
        return self.monthly_payment_amount - self.interest_value
    
    @property
    def monthly_payment(self) -> MonthlyPayment:        
        amount = self.monthly_payment_amount
        interest_value = self.interest_value
        payback_value = min(amount, self.current_amount + interest_value)
        return MonthlyPayment(amount, interest_value, payback_value)

    @property
    def repayment_parameter_set(self) -> ty.Optional[RepaymentParameterSet]:
        return self._repayment_parameter_set.get_value(self._current_date)
    
    def create_follow_up(self, payment_plan: PaymentPlan) -> 'Mortgage':
        if self._follow_up_creator is None:
            raise ValueError(f'Missing follow up creator for {__name__} \'{self.name}\'')
        return self._follow_up_creator(self, payment_plan)
