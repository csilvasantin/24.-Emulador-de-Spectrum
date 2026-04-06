# Proyecto 24 — Emulador de Spectrum

> Herramienta para convertir audio de cinta cassette ZX Spectrum en datos digitales interpretables.

## Contexto
Este proyecto construye un decodificador de audio de cinta ZX Spectrum. Lee archivos WAV, detecta pulsos, clasifica bits (cortos vs. largos), y genera bytes. Es un MVP funcional que sienta las bases para un decodificador completo capaz de recuperar programas y datos de cintas Spectrum reales.

## Arquitectura
- **spectrum_tape_decoder**: módulo Python principal
- Flujo: WAV → normalización → detección de cruces de cero → clasificación de pulsos → bits → bytes
- Soporta entrada mono y estéreo
- Usa umbral automático para distinguir pulsos cortos (bit 0) de largos (bit 1)
- Histéresis en detección de cruces para evitar falsos positivos

## Uso
```bash
cd /Users/csilvasantin/Documents/Codex/Emulador-de-Spectrum
python3 -m spectrum_tape_decoder /ruta/al/audio.wav

# O con límite de bytes:
PYTHONPATH=src python3 -m spectrum_tape_decoder /ruta/al/audio.wav --max-bytes 32
```

## Notas para IAs
- MVP actual no intenta ser decodificador exacto — es una base funcional para iterar
- Próximos pasos: mejorar ruido/variaciones de volumen, detectar cabeceras de Spectrum, separar bloques, validar checksums, exportar a TAP/TZX
- Considerar evolución hacia reconstrucción de programas BASIC desde datos recuperados
- Cada iteración debe mantener compatibilidad con archivos WAV reales de cintas Spectrum
