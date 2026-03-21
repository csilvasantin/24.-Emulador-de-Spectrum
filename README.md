# Emulador de Spectrum

Proyecto para leer el sonido de una cinta de cassette de ZX Spectrum y convertirlo en datos digitales interpretables.

## Objetivo

Construir una herramienta que:

1. lea el audio de una carga de cinta;
2. detecte pulsos;
3. convierta esos pulsos en bits;
4. agrupe bits en bytes;
5. permita evolucionar hacia bloques reales de Spectrum (`TAP`/`TZX` o reconstrucción de programas).

## Estado actual

Este repositorio arranca con un MVP que:

- lee archivos WAV mono o estéreo;
- normaliza la señal;
- detecta cruces de signo y estima la duración de pulsos;
- clasifica pulsos cortos y largos usando un umbral automático;
- genera una secuencia estimada de bits;
- empaqueta bits en bytes;
- muestra un resumen por consola.

No pretende todavía ser un decodificador completo y exacto del formato de cinta de Spectrum. Es una base funcional para iterar.

## Uso

```bash
cd /Users/csilvasantin/Documents/Codex/Emulador-de-Spectrum
python3 -m spectrum_tape_decoder /ruta/al/audio.wav
```

También puedes pedir una vista más corta:

```bash
PYTHONPATH=src python3 -m spectrum_tape_decoder /ruta/al/audio.wav --max-bytes 32
```

## Qué hace el decoder ahora

- extrae la señal del WAV;
- detecta medias ondas mediante cruces de cero con histéresis;
- suma pares de medias ondas para estimar pulsos completos;
- intenta separar pulsos cortos y largos;
- convierte esa diferencia en bits `0` y `1`;
- agrupa cada 8 bits en un byte.

## Siguientes pasos recomendados

1. soportar mejor ruido y variaciones de volumen;
2. detectar cabeceras reales de cinta de Spectrum;
3. separar bloques;
4. validar checksums;
5. exportar a un formato más estándar;
6. intentar reconstruir listados BASIC o datos.
