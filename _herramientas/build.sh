#!/bin/sh
# Regenera todas las páginas de Finanzas con Lucas con la marca aplicada
set -e; cd /home/claude/apps
python3 gen.py >/dev/null; python3 gen2.py; python3 gen3.py; python3 vivo.py >/dev/null; python3 marca_apps.py >/dev/null; python3 og.py >/dev/null; echo listo
