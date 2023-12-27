import unittest as ut

from mortgage_sim.FinancialDate import FinancialDate
from mortgage_sim.FinancialDelta import FinancialDelta
from mortgage_sim.TemporalValue import TemporalValue
from mortgage_sim.Finances import Finances


class FinancialDateTest(ut.TestCase):
    def test_delta(self):        
        # Arrange
        fst = FinancialDate(year=2024, month=12)
        snd = FinancialDate(year=2025, month=1)
        
        # Act
        delta: FinancialDelta = snd - fst
        neg_delta: FinancialDelta = fst - snd
        
        # Assert
        self.assertIsInstance(delta, FinancialDelta)
        self.assertEqual(delta.months, 1)
        
        self.assertIsInstance(neg_delta, FinancialDelta)
        self.assertEqual(neg_delta.months, -1)
        
    def test_add(self):
        # Arrange
        date = FinancialDate(year=2024, month=12)
        expected_dates = [(12, 2024), (1, 2025), (2, 2025), (3, 2025), 
                          (4, 2025), (5, 2025), (6, 2025), (7, 2025), 
                          (8, 2025), (9, 2025), (10, 2025), (11, 2025), 
                          (12, 2025), (1, 2026), (2, 2026), (3, 2026), 
                          (4, 2026), (5, 2026)]
        
        # Act
        new_dates = list()
        for m in range(0, 18):
            new_dates.append(date + FinancialDelta(months=m))
        
        # Assert
        for i, new_date in enumerate(new_dates):
            expected_month, expected_year = expected_dates[i]
            self.assertIsInstance(new_date, FinancialDate)
            self.assertEqual(new_date.year, expected_year)
            self.assertEqual(new_date.month, expected_month)

class TemporalValueTest(ut.TestCase):
    def test_temporal_value(self):
        # Arrange
        default_value = -1
        expected_value = 20
        
        tv = TemporalValue[int](default_value)
        before_date = FinancialDate(year=2023, month=12)
        date = FinancialDate(year=2024, month=1)
        after_date = FinancialDate(year=2024, month=2)
        
        # Act
        tv.set_value(date, expected_value)
        
        # Assert
        self.assertEqual(tv.get_value(before_date), default_value)
        self.assertEqual(tv.get_value(date), expected_value)
        self.assertEqual(tv.get_value(after_date), expected_value)
        
        
class FinancesTest(ut.TestCase):
    def test_check_finances(self):
        # Arrange
        expected_balances = [
            5_950 + 715 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Jan 24
            5_950 + 715 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Feb 24
            5_950 + 715 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Mar 24
            5_950 + 715 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Apr 24
            6_350 + 715 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # May 24
            6_350 + 3_000 + 715 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Jun 24
            6_350 + 715 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Jul 24
            6_350 + 715 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Aug 24
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Sep 24
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Oct 24
            6_350 + 3_000 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Nov 24
            6_350 + 3_000 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460), # Dec 24
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Jan 25
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Feb 25
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Mar 25
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Apr 25
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # May 25
            6_350 + 3_000 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Jun 25
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Jul 25
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Aug 25
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Sep 25
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Oct 25
            6_350 + 3_000 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Nov 25
            6_350 + 3_000 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460), # Dec 25
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Jan 26
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Feb 26
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Mar 26
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Apr 26
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # May 26
            6_350 + 3_000 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Jun 26
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Jul 26
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Aug 26
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Sep 26
            6_350 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Oct 26
            6_350 + 3_000 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460),  # Nov 26
            6_350 + 3_000 + 250 - (952 + 170 + 2_000 + 110 + 340 + 25 + 20 + 460), # Dec 26
        ]
        start_date = FinancialDate(year=2024, month=1)
        finances = Finances(0) \
            .add_income('Gehalt: Ralf', start_date, 5_950, FinancialDelta(months=1)) \
            .add_income('Urlaubsgeld: Ralf', start_date + FinancialDelta(months=5), 3_000, FinancialDelta(months=12)) \
            .add_income('Weihnachtsgeld: Ralf', start_date + FinancialDelta(months=10), 3_000, FinancialDelta(months=12)) \
            .add_income('Dankesprämie: Ralf', start_date + FinancialDelta(months=11), 3_000, FinancialDelta(months=12)) \
            .add_income('Gehalt: Ralf', FinancialDate(year=2024, month=5), 6_350, FinancialDelta(months=1)) \
            .add_income('Elterngeld: Caro', start_date, 715, FinancialDelta(months=1)) \
            .add_income('Kindergeld', start_date, 250, FinancialDelta(months=1)) \
            .remove_income('Elterngeld: Caro', FinancialDate(year=2024, month=9))\
            .add_expense('Privatversicherung', start_date, 952, FinancialDelta(months=1)) \
            .add_expense('Sonstige Versicherungen', start_date, 170, FinancialDelta(months=1)) \
            .add_expense('Lebenshaltung', start_date, 2_000, FinancialDelta(months=1)) \
            .add_expense('Nebenkosten', start_date, 110, FinancialDelta(months=1)) \
            .add_expense('Heizkosten', start_date, 340, FinancialDelta(months=1)) \
            .add_expense('Risikolebensversicherung', start_date, 25, FinancialDelta(months=1)) \
            .add_expense('Gebäudeversicherung', start_date, 20, FinancialDelta(months=1)) \
            .add_expense('Altersvorsorge', start_date, 460, FinancialDelta(months=1))
            
        # Act
        balances = list()
        for m in range(36):
            balance = finances.get_effective_balance(start_date + FinancialDelta(months=m))
            balances.append(balance)
            
        # Assert
        for i in range(36):
            actual_balance = balances[i]
            expected_balance = expected_balances[i]
            self.assertEqual(actual_balance, expected_balance, f'Error at index {i}')
        

if __name__ == '__main__':
    ut.main()
