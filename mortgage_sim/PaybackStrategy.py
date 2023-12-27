import abc
import pandas as pd
import typing as ty

from decimal import Decimal

from mortgage_sim.Finances import Finances
from mortgage_sim.FinancialDate import FinancialDate
from mortgage_sim.FinancialDelta import FinancialDelta

from mortgage_sim.Mortgage import Mortgage
from mortgage_sim.PaymentPlan import PaymentPlan
from mortgage_sim.Wallet import Wallet


class PaybackStrategy(abc.ABC):
    def __init__(self, mortgages: ty.List[Mortgage]) -> None:
        self._mortgages: ty.List[Mortgage] = mortgages
        self._mortgages_history: ty.List[Mortgage] = list(mortgages)
                    
    @property
    def _is_active(self) -> bool:
        return any(Decimal(0) < mortgage.current_amount for mortgage in self._mortgages)
    
    def _is_valid_mortgage(self, current_date: FinancialDate, mortgage: Mortgage):
        return mortgage.valid_from is None or mortgage.valid_from <= current_date
    
    def calculate_payment_plan(self, start: FinancialDate, finances: Finances, wallet: Wallet) -> pd.DataFrame:     
        payment_plan = PaymentPlan()
           
        for month in range(0, 30 * 12):
            current_date = start + FinancialDelta(months=month)
            
            for mortgage in self._mortgages:
                mortgage.update_current_date(current_date)
            
            if not self._is_active:
                break
            
            # Start a new row
            payment_plan.start_of_row()
            
            # Record income, expense and balance
            y, m = divmod(month, 12)
            payment_plan.record('Date', current_date)
            payment_plan.record('Month', int(month))
            payment_plan.record('Delta', f'{y:02d}\'{m:02d}\'\'')
            payment_plan.record('Wallet', wallet.current_amount)
            payment_plan.record('Income', finances.get_effective_income_value(current_date))
            payment_plan.record('Expense', finances.get_effective_expense_value(current_date))
            payment_plan.record('Balance', finances.get_effective_balance(current_date))
            
            wallet += finances.get_effective_balance(current_date)
            
            # Execute payments
            self._payback(current_date, payment_plan, wallet)
            
            if wallet.current_amount < Decimal(0):
                raise Exception(f'Overextension: {wallet.current_amount}')
        
        column_order = ['Date', 'Month', 'Delta', 'Wallet', 'Income', 'Expense', 'Balance', 'Interest Sum', 'Mortgage Sum', 'Payment Sum']
        for mortgage in self._mortgages_history:
            column_order += mortgage.columns()
        
        return payment_plan.result[column_order]
    
    @abc.abstractmethod
    def _unscheduled_payments_order(self, mortgages: ty.List[Mortgage]) -> ty.List[Mortgage]:
        return None
            
    def _payback(self, current_date: FinancialDate, payment_plan: PaymentPlan, wallet: Wallet) -> None:
        # Replace mortgage if it is no more valid
        del_indices = []
        for index, mortgage in enumerate(self._mortgages):
            if mortgage.valid_until is None or current_date < mortgage.valid_until or mortgage.current_amount == Decimal(0):
                continue
            del_indices.append(index)
            new_mortgage = mortgage.create_follow_up(payment_plan)
            if new_mortgage is None:
                continue
            new_mortgage.update_current_date(current_date)
            self._mortgages.append(new_mortgage)
            self._mortgages_history.append(new_mortgage)
            
        # Remove obsolete mortgages
        for index in sorted(del_indices, reverse=True):
            del self._mortgages[index]
        
        # Get only the valid mortgages
        valid_mortgages = [mortgage for mortgage in self._mortgages if self._is_valid_mortgage(current_date, mortgage)]
        
        # Sum monthly payment
        interest_sum = sum(mortgage.interest_value for mortgage in valid_mortgages)
        payment_plan.record('Interest Sum', interest_sum, 0)
        
        mortgage_sum = sum(mortgage.current_amount for mortgage in valid_mortgages)
        payment_plan.record('Mortgage Sum', mortgage_sum, 0)
        
        payment_sum = sum(mortgage.monthly_payment.payback_value for mortgage in valid_mortgages)
        payment_plan.record('Payment Sum', payment_sum, 0)
                
        # Pay mortgage if needed
        for mortgage in valid_mortgages:
            mortgage.execute_payback(payment_plan, wallet)
            
        # Unscheduled payments
        for mortgage in self._unscheduled_payments_order(valid_mortgages):
            mortgage.execute_unscheduled_payment(payment_plan, wallet)
        

