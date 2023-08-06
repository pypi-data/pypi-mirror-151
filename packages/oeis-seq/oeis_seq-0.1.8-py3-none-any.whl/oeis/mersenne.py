from typing import Iterable

from oeis.registry import registry

from .eratosthenes import eratosthenes


@registry.register(identifier="A001348")
def mersenne() -> Iterable[int]:
    """Mersenne numbers."""
    for n in eratosthenes():  # pragma: no branch
        yield pow(2, n) - 1
