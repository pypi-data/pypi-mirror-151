"""OEIS Sequences."""
from .abundant import abundant
from .arithmetic import arithmetic
from .buttered_croissant import buttered_croissant
from .carmichael import carmichael
from .catalan import catalan
from .centered_polygonal import (
    centered_decagonal,
    centered_dodecagonal,
    centered_hendecagonal,
    centered_heptagonal,
    centered_hexagonal,
    centered_nonagonal,
    centered_octagonal,
    centered_pentagonal,
    centered_polygonal,
    centered_square,
    centered_triangular,
)
from .composite import composite
from .deficient import deficient
from .eratosthenes import eratosthenes
from .factorial import factorial
from .fermat import fermat
from .fibonacci import fibonacci
from .hilbert import hilbert
from .icosahedral import icosahedral
from .jacobsthal import jacobsthal
from .kynea import kynea
from .lazy_caterer import lazy_caterer
from .leonardo import leonardo
from .loeschian import loeschian
from .lucas import lucas
from .mersenne import mersenne
from .oblong import oblong
from .padovan import padovan
from .pell import pell
from .perfect import perfect
from .period2 import period2
from .perrin import perrin
from .polite import polite
from .polygonal import (
    decagonal,
    dodecagonal,
    hendecagonal,
    heptagonal,
    hexagonal,
    natural,
    nonagonal,
    octagonal,
    pentagonal,
    polygonal,
    square,
    triangular,
)
from .pyramidal import (
    heptagonal_pyramidal,
    hexagonal_pyramidal,
    octagonal_pyramidal,
    pentagonal_pyramidal,
    square_pyramidal,
    triangular_pyramidal,
)
from .quasiperfect import quasiperfect
from .recaman import recaman
from .rough import (
    rough,
    rough2,
    rough3,
    rough5,
    rough7,
    rough11,
    rough13,
    rough17,
    rough19,
    rough23,
)
from .semiperfect import semiperfect
from .smooth import (
    smooth,
    smooth2,
    smooth3,
    smooth5,
    smooth7,
    smooth11,
    smooth13,
    smooth17,
    smooth19,
    smooth23,
)
from .sorting import sorting
from .superperfect import superperfect
from .sylvester import sylvester
from .totient import totient
from .tribonacci import tribonacci
from .unusual import unusual
from .vauban import vauban
from .weird import weird
from .woodall import woodall

__version__ = "0.1.8"
__all__ = [
    "abundant",
    "arithmetic",
    "buttered_croissant",
    "carmichael",
    "catalan",
    "centered_decagonal",
    "centered_dodecagonal",
    "centered_hendecagonal",
    "centered_heptagonal",
    "centered_hexagonal",
    "centered_nonagonal",
    "centered_octagonal",
    "centered_pentagonal",
    "centered_polygonal",
    "centered_square",
    "centered_triangular",
    "composite",
    "decagonal",
    "deficient",
    "dodecagonal",
    "eratosthenes",
    "factorial",
    "fermat",
    "fibonacci",
    "hendecagonal",
    "heptagonal",
    "heptagonal_pyramidal",
    "hexagonal",
    "hexagonal_pyramidal",
    "hilbert",
    "icosahedral",
    "jacobsthal",
    "kynea",
    "lazy_caterer",
    "leonardo",
    "loeschian",
    "lucas",
    "mersenne",
    "natural",
    "nonagonal",
    "oblong",
    "octagonal",
    "octagonal_pyramidal",
    "padovan",
    "pell",
    "pentagonal",
    "pentagonal_pyramidal",
    "perfect",
    "period2",
    "perrin",
    "polite",
    "polygonal",
    "quasiperfect",
    "recaman",
    "rough",
    "rough2",
    "rough3",
    "rough5",
    "rough7",
    "rough11",
    "rough13",
    "rough17",
    "rough19",
    "rough23",
    "semiperfect",
    "smooth",
    "smooth2",
    "smooth3",
    "smooth5",
    "smooth7",
    "smooth11",
    "smooth13",
    "smooth17",
    "smooth19",
    "smooth23",
    "sorting",
    "square",
    "sylvester",
    "square_pyramidal",
    "superperfect",
    "totient",
    "triangular",
    "triangular_pyramidal",
    "tribonacci",
    "unusual",
    "vauban",
    "weird",
    "woodall",
]
