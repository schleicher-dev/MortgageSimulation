from mortgage_sim.TemporalValue import TemporalValue


import typing as ty


TValue = ty.TypeVar('TValue')


class NamedTemporalValue(TemporalValue[TValue]):
    def __init__(self, name: str, default_value: ty.Optional[TValue]) -> None:
        super().__init__(default_value)
        self._name: str = name

    @property
    def name(self) -> str:
        return self._name
    
    def __repr__(self) -> str:
        return f'<{__name__} name={self.name} default_value={self._default_value} collection={self._collection}>'