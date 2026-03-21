from __future__ import annotations

import argparse
from pathlib import Path

from .decoder import decode_wav


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lee un WAV de cinta de Spectrum y estima pulsos, bits y bytes."
    )
    parser.add_argument("input_wav", type=Path, help="Ruta al archivo WAV de entrada.")
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=64,
        help="Número máximo de bytes a mostrar en la salida.",
    )
    return parser


def _format_hex_preview(values: list[int], max_bytes: int) -> str:
    visible = values[:max_bytes]
    preview = " ".join(f"{value:02X}" for value in visible)
    if len(values) > max_bytes:
        return f"{preview} ..."
    return preview or "(sin bytes detectados)"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.input_wav.exists():
        parser.error(f"No existe el archivo: {args.input_wav}")

    result = decode_wav(args.input_wav)

    print("Resumen de decodificación")
    print(f"- Archivo: {args.input_wav}")
    print(f"- Sample rate: {result.sample_rate} Hz")
    print(f"- Muestras: {result.sample_count}")
    print(f"- Pulsos detectados: {len(result.pulse_lengths_us)}")
    print(f"- Umbral estimado: {result.threshold_us:.2f} us")
    print(f"- Bits estimados: {len(result.bits)}")
    print(f"- Bytes estimados: {len(result.bytes_out)}")
    print(f"- Vista previa HEX: {_format_hex_preview(result.bytes_out, args.max_bytes)}")

    return 0
