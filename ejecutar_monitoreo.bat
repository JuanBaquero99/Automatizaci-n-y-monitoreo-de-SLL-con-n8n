@echo off
echo 🚨 === MONITOREO SSL SEMANAL ===
echo Fecha: %date% %time%
echo.

echo 🔍 Verificando certificados SSL de 20 clientes...
python scripts\verificar_ssl.py

echo.
echo 📧 Verificando si hay alertas que enviar...
python scripts\enviar_alertas.py

echo.
echo ✅ Proceso completado!
echo Revisa el resultado arriba para ver el estado de los certificados.
pause
