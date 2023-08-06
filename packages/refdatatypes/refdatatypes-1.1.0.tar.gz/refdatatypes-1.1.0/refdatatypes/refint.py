from refdatatypes.refbase import RefBase


class RefInt(RefBase):
    def __init__(self, value_: int):
        super().__init__(value_)

    @property
    def value(self) -> int:
        return super().value

    @value.setter
    def value(self, value_: int):
        super()._base_value_setter(int(value_))
