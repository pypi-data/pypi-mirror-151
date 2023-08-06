def safe_int(value: str, default_value: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return int(default_value)


def safe_float(value: str, default_value: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default_value)


def safe_bool(value: str, default_value: bool = False) -> bool:
    try:
        return bool(value)
    except (TypeError, ValueError):
        return bool(default_value)


class SafeDict(dict):
    def __init__(self, init_data: dict = None, default_value=None, autoset: bool = False):
        self._default_value = default_value
        self._autoset = autoset
        if init_data:
            self.update(init_data)

    def __getitem__(self, item: str):
        try:
            return super().__getitem__(item)
        except KeyError:
            if self._autoset:
                self.__setitem__(item, self._default_value)
            return self._default_value


class SafeList(list):
    def __init__(self, init_data: list = None, default_value=None):
        self._default_value = default_value
        if init_data:
            self.extend(init_data)

    def __getitem__(self, item: str):
        try:
            return super().__getitem__(item)
        except IndexError:
            return self._default_value
