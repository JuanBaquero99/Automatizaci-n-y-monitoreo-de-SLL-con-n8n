#!/bin/bash

echo "🚀 Configurando repositorio para Railway deployment..."

# Inicializar git si no existe
if [ ! -d ".git" ]; then
    echo "📝 Inicializando repositorio Git..."
    git init
fi

# Crear .gitignore
echo "📝 Creando .gitignore..."
cat > .gitignore << EOF
# Environment variables
.env
.env.local
.env.production

# Node modules
node_modules/
npm-debug.log*

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.coverage
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite

# Temporary files
tmp/
temp/
EOF

# Agregar archivos al staging
echo "📦 Agregando archivos al repositorio..."
git add .

# Commit inicial
echo "💾 Creando commit inicial..."
git commit -m "🎉 Sistema de monitoreo SSL inicial

- Scripts Python para verificación SSL
- Workflow n8n automatizado  
- Configuración Docker para Railway
- Sistema de alertas por email
- Base de datos de 20 clientes"

echo "✅ Repositorio configurado exitosamente!"
echo ""
echo "🔗 Próximos pasos:"
echo "1. Crear repositorio en GitHub"
echo "2. git remote add origin <URL_GITHUB>"
echo "3. git push -u origin main"
echo "4. Conectar Railway a GitHub"
echo "5. Deploy automático!"
