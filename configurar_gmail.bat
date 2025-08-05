@echo off
echo 📧 Configurando Gmail para alertas SSL...
echo.

echo Configura estas 3 variables con tus datos:
echo.
echo 1. Tu email de Gmail:
set /p EMAIL_USER="EMAIL_USER (tu-email@gmail.com): "

echo.
echo 2. App Password de Gmail (generar en Gmail > Seguridad):
set /p EMAIL_PASSWORD="EMAIL_PASSWORD (16 caracteres): "

echo.
echo 3. Email donde recibir alertas:
set /p EMAIL_DESTINATARIO="EMAIL_DESTINATARIO (alertas@empresa.com): "

echo.
echo ✅ Configuración guardada para esta sesión
echo.
echo 🧪 Probando configuración...
python scripts\enviar_alertas.py

pause
