from itertools import count
from typing import Iterable

from oeis.registry import registry
from oeis.utils import is_semiperfect


@registry.register("A005835")
def semiperfect() -> Iterable[int]:
    """Semiperfect numbers."""
    for n in count(start=1):  # pragma: no branch
        if is_semiperfect(n):
            yield n
