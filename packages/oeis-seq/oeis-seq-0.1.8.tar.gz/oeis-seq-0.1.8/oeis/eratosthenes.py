from typing import Dict, Iterable, List

from oeis.registry import registry


@registry.register("A000040")
def eratosthenes() -> Iterable[int]:
    """Sieve of Eratosthenes."""
    discards: Dict[int, List[int]] = {}
    p: int = 2

    while True:
        if p not in discards:
            yield p
            discards[p * p] = [p]
        else:
            for n in discards[p]:
                discards.setdefault(p + n, []).append(n)
            del discards[p]
        p += 1
