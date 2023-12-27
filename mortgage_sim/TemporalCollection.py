from mortgage_sim.FinancialDate import FinancialDate
from mortgage_sim.NamedTemporalValue import NamedTemporalValue


import typing as ty
from datetime import datetime


TValue = ty.TypeVar('TValue')


class TemporalCollection(ty.Generic[TValue]):
    def __init__(self) -> None:
        self._collection: ty.Dict[str, NamedTemporalValue[TValue]] = dict()
        
    def set_value(self, key: str, when: FinancialDate, value: TValue) -> None:
        entry = self._collection.get(key, None)
        if entry is None:
            self._collection[key] = entry = NamedTemporalValue(key, None)
        entry.set_value(when, value)

    def values(self, when: datetime) -> ty.Generator[ty.Tuple[str, TValue], None, None]:
        for temporal_value in self._collection.values():
            value = temporal_value.get_value(when)
            if value is None:
                continue
            yield (temporal_value.name, value)