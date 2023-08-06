from itertools import count
from typing import Iterable, List

from oeis.registry import registry

from .utils import is_prime, prime_factors


def smooth(n: int) -> Iterable[int]:
    """
    n-smooth numbers.

    Args:
            n: prime integer.
    """
    if not is_prime(n):
        raise ValueError("n must be a prime number.")

    yield 1
    for k in count(start=2):  # pragma: no branch
        factors: List[int] = prime_factors(k)
        max_prime = max(factors)
        if max_prime <= n:
            yield k


@registry.register("A000079")
def smooth2() -> Iterable[int]:
    """2-smooth numbers."""
    return smooth(2)


@registry.register("A003586")
def smooth3() -> Iterable[int]:
    """3-smooth numbers, also known as Harmonic numbers."""
    return smooth(3)


@registry.register("A051037")
def smooth5() -> Iterable[int]:
    """5-smooth numbers, also known as Hamming numbers."""
    return smooth(5)


@registry.register("A002473")
def smooth7() -> Iterable[int]:
    """7-smooth numbers, also known as Humble numbers."""
    return smooth(7)


@registry.register("A051038")
def smooth11() -> Iterable[int]:
    """11-smooth numbers."""
    return smooth(11)


@registry.register("A080197")
def smooth13() -> Iterable[int]:
    """13-smooth numbers."""
    return smooth(13)


@registry.register("A080681")
def smooth17() -> Iterable[int]:
    """17-smooth numbers."""
    return smooth(17)


@registry.register("A080682")
def smooth19() -> Iterable[int]:
    """19-smooth numbers."""
    return smooth(19)


@registry.register("A080683")
def smooth23() -> Iterable[int]:
    """23-smooth numbers."""
    return smooth(23)
