#!/bin/sh
# Script de inicio para n8n en Render

# Crear directorio de configuración si no existe
mkdir -p /home/node/.n8n

# Inicializar n8n con configuración básica
echo "Iniciando n8n..."

# Ejecutar n8n
exec /usr/local/bin/n8n start
