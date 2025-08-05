#!/bin/bash
echo "🚨 === MONITOREO SSL SEMANAL ==="
echo "Fecha: $(date)"
echo ""

echo "🔍 Verificando certificados SSL de 20 clientes..."
python3 scripts/verificar_ssl.py

echo ""
echo "📧 Verificando si hay alertas que enviar..."
python3 scripts/enviar_alertas.py

echo ""
echo "✅ Proceso completado!"
echo "Revisa el resultado arriba para ver el estado de los certificados."
