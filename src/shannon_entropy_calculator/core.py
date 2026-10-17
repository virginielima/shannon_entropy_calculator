"""Core entropy calculation routines.

We treat the input string as a sequence of Unicode *code points* (Python's
str). Each distinct code point is one symbol in the alphabet. Entropy is
reported in bits when natural-log math is converted by the factor 1/ln(2).

Design choices
--------------
* math.log is used (not precomputed tables) so the library stays correct for
  any alphabet the input happens to contain, including exotic Unicode.
* An empty input returns 0.0 rather than raising — a zero-length signal
  carries no information, and callers checking "is this random?" expect a
  number, not an exception.
* Python floats are returned directly; we do not quantise, so callers can
  compare with their own tolerance.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Iterable


def shannon_entropy_bits(data: str) -> float:
    """Return the Shannon entropy of *data* in bits per symbol.

    Parameters
    ----------
    data:
        The input string. Each distinct Unicode code point is treated as one
        symbol. The empty string returns 0.0.

    Returns
    -------
    float
        Entropy value in bits (log base 2). For a string with k equally
        frequent distinct symbols the result is log2(k). For a string where
        every symbol is identical the result is 0.0.
    """
    n = len(data)
    if n == 0:
        return 0.0
    counts = Counter(data)
    # With a single distinct symbol, every probability is 1 and p*log2(p) is
    # 0, but we short-circuit to avoid the -inf*0 edge entirely.
    if len(counts) == 1:
        return 0.0
    entropy = 0.0
    inv = 1.0 / n
    for _symbol, count in counts.items():
        p = count * inv
        entropy -= p * math.log(p, 2)
    return entropy


def shannon_entropy(data: str) -> float:
    """Alias for :func:`shannon_entropy_bits`.

    Provided so callers can write the conceptually-neutral name when they do
    not care about the unit; the unit is still bits.
    """
    return shannon_entropy_bits(data)
