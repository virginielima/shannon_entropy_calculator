import math
import unittest

from shannon_entropy_calculator import shannon_entropy, shannon_entropy_bits
from shannon_entropy_calculator.core import shannon_entropy_bits as core_bits


class TestShannonEntropy(unittest.TestCase):
    def test_empty_string_returns_zero(self):
        self.assertEqual(shannon_entropy(""), 0.0)
        self.assertIsInstance(shannon_entropy(""), float)

    def test_single_symbol_returns_zero(self):
        self.assertEqual(shannon_entropy("a"), 0.0)
        self.assertEqual(shannon_entropy("aaaa"), 0.0)
        self.assertEqual(shannon_entropy("\u0000" * 10), 0.0)

    def test_two_equally_frequent_symbols_is_one_bit(self):
        # "ab" has two equally likely symbols -> entropy = log2(2) = 1.0
        result = shannon_entropy("ab")
        self.assertAlmostEqual(result, 1.0, places=12)

    def test_four_equally_frequent_symbols_is_two_bits(self):
        result = shannon_entropy("abcd")
        self.assertAlmostEqual(result, 2.0, places=12)

    def test_repeated_uniform_block(self):
        # "aabbccdd" -> 4 equally likely symbols -> 2.0 bits
        result = shannon_entropy("aabbccdd")
        self.assertAlmostEqual(result, 2.0, places=12)

    def test_long_uniform_alternating(self):
        # 256 symbols, 2 distinct, equally likely -> 1.0 bit
        data = "ab" * 128
        self.assertAlmostEqual(shannon_entropy(data), 1.0, places=12)

    def test_high_entropy_random_like(self):
        # A 16-symbol alphabet uniformly used -> 4.0 bits
        symbols = "0123456789abcdef"
        data = symbols * 4  # 64 chars, 16 distinct, uniform
        self.assertAlmostEqual(shannon_entropy(data), 4.0, places=12)

    def test_uneven_distribution_is_between_zero_and_max(self):
        # "aaab" -> p(a)=0.75, p(b)=0.25 -> H = 0.811278...
        expected = -(0.75 * math.log2(0.75) + 0.25 * math.log2(0.25))
        result = shannon_entropy("aaab")
        self.assertAlmostEqual(result, expected, places=12)
        self.assertGreater(result, 0.0)
        self.assertLess(result, 1.0)

    def test_returns_float_type(self):
        self.assertIsInstance(shannon_entropy("abc"), float)
        self.assertIsInstance(shannon_entropy_bits("abc"), float)

    def test_alias_matches_core(self):
        self.assertEqual(shannon_entropy("hello"), core_bits("hello"))

    def test_unicode_code_points_are_distinct_symbols(self):
        # Three distinct code points, each appears twice -> log2(3)
        data = "ααββγγ"
        self.assertAlmostEqual(shannon_entropy(data), math.log2(3), places=12)

    def test_combined_emoji_and_ascii(self):
        # Two distinct symbols equally frequent -> 1.0 bit
        data = "a😀" * 5
        self.assertAlmostEqual(shannon_entropy(data), 1.0, places=12)

    def test_max_entropy_for_byte_like_sample(self):
        # 8 distinct symbols uniformly distributed -> 3.0 bits
        data = "abcdefgh"
        self.assertAlmostEqual(shannon_entropy(data), 3.0, places=12)


if __name__ == "__main__":
    unittest.main()
