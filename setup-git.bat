@echo off
echo 🚀 Configurando repositorio para Railway deployment...

REM Inicializar git si no existe
if not exist ".git" (
    echo 📝 Inicializando repositorio Git...
    git init
)

REM Crear .gitignore
echo 📝 Creando .gitignore...
(
echo # Environment variables
echo .env
echo .env.local
echo .env.production
echo.
echo # Node modules
echo node_modules/
echo npm-debug.log*
echo.
echo # Python
echo __pycache__/
echo *.pyc
echo *.pyo
echo *.pyd
echo .Python
echo *.so
echo .coverage
echo .pytest_cache/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo.
echo # Logs
echo *.log
echo logs/
echo.
echo # Database
echo *.db
echo *.sqlite
echo.
echo # Temporary files
echo tmp/
echo temp/
) > .gitignore

REM Agregar archivos al staging
echo 📦 Agregando archivos al repositorio...
git add .

REM Commit inicial
echo 💾 Creando commit inicial...
git commit -m "🎉 Sistema de monitoreo SSL inicial - Scripts Python para verificación SSL - Workflow n8n automatizado - Configuración Docker para Railway - Sistema de alertas por email - Base de datos de 20 clientes"

echo ✅ Repositorio configurado exitosamente!
echo.
echo 🔗 Próximos pasos:
echo 1. Crear repositorio en GitHub
echo 2. git remote add origin URL_GITHUB
echo 3. git push -u origin main
echo 4. Conectar Railway a GitHub
echo 5. Deploy automático!

pause
