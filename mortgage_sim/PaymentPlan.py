from decimal import Decimal

import numpy as np
import pandas as pd
import typing as ty


class PaymentPlan(object):    
    class _Column(object):
        def __init__(self, name: str, default_value: ty.Any, values: ty.List[ty.Any]) -> None:
            self._name: str = name
            self._default_value: ty.Any = default_value
            self._values: ty.List[ty.Any] = values
            
        @property
        def name(self) -> str:
            return self._name
            
        @property
        def default_value(self) -> ty.Any:
            return self._default_value
            
        @property
        def values(self) -> ty.List[ty.Any]:
            return self._values
        
        def start_of_row(self):
            self._values.append(self._default_value)
            
        def record(self, value: ty.Any):
            self._values[-1] = value
        
    def __init__(self) -> None:
        self._columns: ty.Dict[str, PaymentPlan._Column] = dict()
        self._row_index: int = -1
                
    def start_of_row(self):
        self._row_index += 1
        for column in self._columns.values():
            column.start_of_row()
        
    def record(self, column_name: str, value: ty.Any, default_value: ty.Optional[ty.Any] = None):
        if self._row_index < 0:
            raise ValueError('Row Index is -1. Please call start_of_row first.')
        
        if column_name not in self._columns.keys():
            self._columns[column_name] = PaymentPlan._Column(column_name, default_value, [default_value for _ in range(0, self._row_index + 1)])
        
        self._columns[column_name].record(value)
        
    @property
    def result(self) -> pd.DataFrame:
        return pd.DataFrame({key: column.values for key, column in self._columns.items()})

