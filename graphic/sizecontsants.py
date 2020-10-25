from typing import Iterable, Tuple


class SizeConstants:
    SIZE_PRESET = (('SIZE_EMPTY', 0.4),
                   ('SIZE_ACTIVE', 0.61),
                   ('SIZE_INACTIVE', 0.6),
                   ('SIZE_CAPTURED', 0.45))

    def __init__(self, size_preset: Iterable[Tuple[str, float]] = SIZE_PRESET):
        self._sizes = dict(size_preset)

    def __contains__(self, item: str) -> bool:
        return item in self._sizes

    def __getitem__(self, item: str) -> float:
        return self._sizes[item]
