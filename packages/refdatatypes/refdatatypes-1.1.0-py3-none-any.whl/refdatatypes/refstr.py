from refdatatypes.refbase import RefBase


class RefStr(RefBase):
    def __init__(self, value_: str):
        super().__init__(value_)

    @property
    def value(self) -> str:
        return super().value

    @value.setter
    def value(self, value_: str):
        super()._base_value_setter(str(value_))
