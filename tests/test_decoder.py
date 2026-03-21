import unittest

from spectrum_tape_decoder.decoder import bits_to_bytes, estimate_threshold, pulses_to_bits


class DecoderTests(unittest.TestCase):
    def test_pulses_to_bits_uses_threshold(self) -> None:
        pulses = [900.0, 950.0, 1800.0, 1900.0]
        threshold = estimate_threshold(pulses)
        self.assertEqual(pulses_to_bits(pulses, threshold), [0, 0, 1, 1])

    def test_bits_to_bytes_groups_eight_bits(self) -> None:
        bits = [0, 1, 0, 0, 0, 0, 0, 1]
        self.assertEqual(bits_to_bytes(bits), [0x41])


if __name__ == "__main__":
    unittest.main()
