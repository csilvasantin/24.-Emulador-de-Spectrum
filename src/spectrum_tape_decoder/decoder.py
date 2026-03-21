from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from statistics import median

from .wav_reader import read_wav


@dataclass(frozen=True)
class DecodeResult:
    sample_rate: int
    sample_count: int
    pulse_lengths_us: list[float]
    threshold_us: float
    bits: list[int]
    bytes_out: list[int]


def _signal_state(sample: float, hysteresis: float) -> int:
    if sample > hysteresis:
        return 1
    if sample < -hysteresis:
        return -1
    return 0


def detect_half_waves(samples: list[float], sample_rate: int, hysteresis: float = 0.05) -> list[float]:
    if not samples:
        return []

    last_state = 0
    last_crossing_index: int | None = None
    half_waves_us: list[float] = []

    for index, sample in enumerate(samples):
        state = _signal_state(sample, hysteresis)
        if state == 0:
            continue
        if last_state == 0:
            last_state = state
            last_crossing_index = index
            continue
        if state == last_state:
            continue
        if last_crossing_index is not None:
            duration_samples = index - last_crossing_index
            if duration_samples > 0:
                half_waves_us.append((duration_samples / sample_rate) * 1_000_000.0)
        last_crossing_index = index
        last_state = state

    return half_waves_us


def pair_half_waves(half_waves_us: list[float]) -> list[float]:
    pulse_lengths_us: list[float] = []
    for index in range(0, len(half_waves_us) - 1, 2):
        pulse_lengths_us.append(half_waves_us[index] + half_waves_us[index + 1])
    return pulse_lengths_us


def estimate_threshold(pulse_lengths_us: list[float]) -> float:
    if not pulse_lengths_us:
        return 0.0

    ordered = sorted(pulse_lengths_us)
    midpoint = len(ordered) // 2
    lower = ordered[: midpoint or 1]
    upper = ordered[midpoint:]
    return (median(lower) + median(upper)) / 2.0


def pulses_to_bits(pulse_lengths_us: list[float], threshold_us: float) -> list[int]:
    if threshold_us <= 0:
        return []
    return [0 if pulse <= threshold_us else 1 for pulse in pulse_lengths_us]


def bits_to_bytes(bits: list[int]) -> list[int]:
    byte_values: list[int] = []
    for index in range(0, len(bits) - 7, 8):
        value = 0
        for bit_index, bit in enumerate(bits[index : index + 8]):
            value |= (bit & 1) << (7 - bit_index)
        byte_values.append(value)
    return byte_values


def decode_wav(path: Path) -> DecodeResult:
    sample_rate, samples = read_wav(path)
    half_waves_us = detect_half_waves(samples, sample_rate=sample_rate)
    pulse_lengths_us = pair_half_waves(half_waves_us)
    threshold_us = estimate_threshold(pulse_lengths_us)
    bits = pulses_to_bits(pulse_lengths_us, threshold_us=threshold_us)
    byte_values = bits_to_bytes(bits)
    return DecodeResult(
        sample_rate=sample_rate,
        sample_count=len(samples),
        pulse_lengths_us=pulse_lengths_us,
        threshold_us=threshold_us,
        bits=bits,
        bytes_out=byte_values,
    )
