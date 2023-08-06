from itertools import count
from math import floor, log2
from typing import Iterable

from oeis.registry import registry


@registry.register("A001855")
def sorting() -> Iterable[int]:
    """
    Sorting numbers.

        The maximal number of comparisons for sorting n elements by binary insertion.
    """

    def S(n: int) -> int:
        return floor(1 + log2(n))

    for n in count(start=1):  # pragma: no branch
        yield n * S(n) - pow(2, S(n)) + 1
