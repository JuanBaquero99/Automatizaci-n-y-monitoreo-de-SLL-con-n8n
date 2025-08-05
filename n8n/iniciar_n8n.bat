@echo off
echo ========================================
echo   INICIANDO N8N - MONITOREO CLIENTES
echo ========================================
echo.

echo 📋 Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado o no está funcionando
    echo 📥 Instala Docker Desktop: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo ✅ Docker detectado
echo.

echo 🚀 Iniciando n8n...
cd /d "%~dp0"
docker-compose up -d

echo.
echo ✅ N8N iniciado exitosamente!
echo.
echo 🌐 Accede a n8n en: http://localhost:5678
echo 👤 Usuario: admin
echo 🔑 Contraseña: admin123
echo.
echo 📝 Comandos útiles:
echo    Para detener: docker-compose down
echo    Para ver logs: docker-compose logs -f
echo.
pause
