from __future__ import annotations

import wave
from pathlib import Path


def _convert_sample(raw: bytes, sample_width: int) -> int:
    if sample_width == 1:
        return raw[0] - 128
    if sample_width == 2:
        return int.from_bytes(raw, byteorder="little", signed=True)
    if sample_width == 3:
        padded = raw + (b"\xff" if raw[-1] & 0x80 else b"\x00")
        return int.from_bytes(padded, byteorder="little", signed=True)
    if sample_width == 4:
        return int.from_bytes(raw, byteorder="little", signed=True)
    raise ValueError(f"Ancho de muestra no soportado: {sample_width}")


def read_wav(path: Path) -> tuple[int, list[float]]:
    with wave.open(str(path), "rb") as wav_file:
        channel_count = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        frame_count = wav_file.getnframes()
        raw_frames = wav_file.readframes(frame_count)

    if channel_count < 1:
        raise ValueError("El WAV no contiene canales de audio")

    frame_size = sample_width * channel_count
    if frame_size <= 0:
        raise ValueError("Tamaño de frame inválido")

    amplitude_max = float((1 << (sample_width * 8 - 1)) - 1)
    samples: list[float] = []

    for frame_index in range(0, len(raw_frames), frame_size):
        frame = raw_frames[frame_index : frame_index + frame_size]
        channel_values = []
        for channel_index in range(channel_count):
            start = channel_index * sample_width
            chunk = frame[start : start + sample_width]
            channel_values.append(_convert_sample(chunk, sample_width))
        mono_value = sum(channel_values) / len(channel_values)
        samples.append(mono_value / amplitude_max)

    return sample_rate, samples
