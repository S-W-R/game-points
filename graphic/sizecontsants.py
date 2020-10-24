from typing import Iterable, Tuple


class SizeConstants:
    SIZE_PRESET = (('SIZE_EMPTY', 0.3),
                   ('SIZE_ACTIVE', 0.5),
                   ('SIZE_INACTIVE', 0.46),
                   ('SIZE_CAPTURED', 0.33))

    def __init__(self, size_preset: Iterable[Tuple[str, float]] = SIZE_PRESET):
        self._sizes = dict(size_preset)

    def __contains__(self, item: str) -> bool:
        return item in self._sizes

    def __getitem__(self, item: str) -> float:
        return self._sizes[item]
