from itertools import count
from typing import Iterable, List

from oeis.registry import registry

from .utils import is_prime, prime_factors


def rough(k: int) -> Iterable[int]:
    """
    k-rough numbers.

    Args:
            k: prime integer.
    """
    if not is_prime(k):
        raise ValueError("n must be a prime number.")

    yield 1
    for n in count(start=2):  # pragma: no branch
        factors: List[int] = prime_factors(n)
        min_prime = min(factors)
        if min_prime >= k:
            yield n


@registry.register("A000027")
def rough2() -> Iterable[int]:
    """2-rough numbers."""
    return rough(2)


@registry.register("A005408")
def rough3() -> Iterable[int]:
    """3-rough numbers."""
    return rough(3)


@registry.register("A007310")
def rough5() -> Iterable[int]:
    """5-rough numbers."""
    return rough(5)


@registry.register("A007775")
def rough7() -> Iterable[int]:
    """7-rough numbers."""
    return rough(7)


@registry.register("A008364")
def rough11() -> Iterable[int]:
    """11-rough numbers."""
    return rough(11)


@registry.register("A008365")
def rough13() -> Iterable[int]:
    """13-rough numbers."""
    return rough(13)


@registry.register("A008366")
def rough17() -> Iterable[int]:
    """17-rough numbers."""
    return rough(17)


@registry.register("A166061")
def rough19() -> Iterable[int]:
    """19-rough numbers."""
    return rough(19)


@registry.register("A166063")
def rough23() -> Iterable[int]:
    """23-rough numbers."""
    return rough(23)
