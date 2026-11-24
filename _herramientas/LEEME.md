# Herramientas para regenerar el sitio

Copiar esta carpeta a `/home/claude/apps` y el repo a `/home/claude/finanzas-con-lucas`, instalar `segno` y `playwright` (con Chromium) y correr `./build.sh`.

- `gen.py`, `gen2.py`, `gen3.py`: generan las calculadoras y la app Mis finanzas.
- `vivo.py`: datos que se actualizan solos en cuotas vs contado.
- `marca_apps.py`: encabezado, pie, Bianca pregunta, metadatos e inicio.
- `og.py`: imágenes para compartir.

Datos manuales que quedan: tabla del monotributo en `gen2.py` (cambia en febrero y agosto) y ejemplos de tasas por tipo de préstamo en `gen.py`.
