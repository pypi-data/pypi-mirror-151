from refdatatypes.refbase import RefBase


class Reffloat(RefBase):
    def __init__(self, value_: float):
        super().__init__(value_)

    @property
    def value(self) -> float:
        return super().value

    @value.setter
    def value(self, value_: float):
        super()._base_value_setter(float(value_))
