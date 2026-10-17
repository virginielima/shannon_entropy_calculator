# shannon_entropy_calculator

Computes the Shannon entropy (in bits per symbol) of a string, treating each distinct Unicode code point as one symbol.

```python
from shannon_entropy_calculator import shannon_entropy, shannon_entropy_bits

print(shannon_entropy("aaaa"))   # 0.0
print(shannon_entropy("abcd"))   # 2.0
print(shannon_entropy_bits("aabbccdd"))  # 2.0
```

## Why this exists

A quick entropy number is useful when triaging whether a blob of text is likely compressed, encrypted, or random — all three push entropy toward the maximum for their alphabet. This library gives you that number with zero dependencies and a single, unambiguous definition: the alphabet is the set of distinct Unicode code points in the input, probabilities are empirical frequencies, and the result is in bits (log base 2).

The trade-off: we do not attempt to classify the data, pick a "byte" vs "character" alphabet, or detect encodings. If you feed a UTF-8 byte string through Python as `str`, each byte becomes a one-character symbol, which is usually what you want for entropy-of-bytes checks; if your input is already a Python `str` of text, each code point is a symbol. The caller decides which interpretation by controlling the input.

## Edge cases you will hit

* The empty string returns `0.0`, not an exception. A zero-length signal carries no information.
* A string of a single repeated symbol returns `0.0`.
* Results are raw `float` values and are not rounded; compare with your own tolerance (e.g. `abs(x - expected) < 1e-9`) rather than `==`.

## Exports

* `shannon_entropy_bits(data: str) -> float` — entropy in bits per symbol.
* `shannon_entropy(data: str) -> float` — alias; same unit (bits).
