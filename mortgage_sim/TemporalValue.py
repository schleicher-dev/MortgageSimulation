import typing as ty
from bisect import bisect_left, insort_left
from mortgage_sim.FinancialDate import FinancialDate


TValue = ty.TypeVar('TValue')


class TemporalValue(ty.Generic[TValue]):
    def __init__(self, default_value: ty.Optional[TValue] = None) -> None:
        super().__init__()
        self._collection: ty.List[ty.Tuple[FinancialDate, ty.Optional[TValue]]] = list()
        self._default_value: ty.Optional[TValue] = default_value
        
    def _find(self, when: FinancialDate) -> ty.Optional[int]:
        if not self._collection:
            return None
        
        index = bisect_left(self._collection, when, key=lambda x: x[0])
        if index == len(self._collection):
            return index - 1
        return index
    
    def set_value(self, when: FinancialDate, value: ty.Optional[TValue]) -> ty.Self:
        index = bisect_left(self._collection, when, key=lambda x: x[0])
        if index == len(self._collection):
            self._collection.append((when, value))
            return self
        
        if self._collection[index][0] == when:
            self._collection[index] = (when, value)
            return self
        
        insort_left(self._collection, (when, value), key=lambda x: x[0])
        return self
    
    def get_value(self, when: FinancialDate) -> ty.Optional[TValue]:
        if not self._collection:
            return self._default_value or None
        
        index = bisect_left(self._collection, when, key=lambda x: x[0])
        if index == len(self._collection) or when < self._collection[index][0]:
            return self._collection[index - 1][1] if index != 0 else self._default_value or None
        if index == 0 and when < self._collection[index][0]:
            return self._default_value or None
        return self._collection[index][1]
    
    def __repr__(self) -> str:
        return f'<{__name__} default_value={self._default_value} collection={self._collection}>'
        

    
