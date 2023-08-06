from refdatatypes.refbase import RefBase


class RefBool(RefBase):
    def __init__(self, value_: bool):
        super().__init__(value_)

    @property
    def value(self) -> bool:
        return super().value

    @value.setter
    def value(self, value_: bool):
        super()._base_value_setter(bool(value_))
