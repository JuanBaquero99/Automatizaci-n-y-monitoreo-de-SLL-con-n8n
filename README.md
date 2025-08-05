# 🚀 Sistema de Monitoreo SSL/Hosting - Automatización con n8n

Sistema automatizado para monitorear 21 clientes, incluyendo vencimientos de SSL, hosting y dominios.

## 📋 Características

- ✅ Verificación automática de certificados SSL
- ✅ Detección de proveedores de hosting
- ✅ Alertas por email preventivas
- ✅ Automatización completa con n8n
- ✅ Deployment gratuito en Railway

## 🛠️ Tecnologías

- **Python 3.8+** - Scripts de verificación
- **n8n** - Automatización de workflows
- **Railway** - Hosting gratuito
- **PostgreSQL** - Base de datos
- **Gmail SMTP** - Envío de alertas

## 🚀 Deploy Rápido en Railway

### 1. Preparar el repositorio

```bash
git init
git add .
git commit -m "Sistema de monitoreo SSL inicial"
```

### 2. Conectar a Railway

1. Ir a [railway.app](https://railway.app)
2. Conectar con GitHub
3. Deploy from GitHub repo
4. Seleccionar `JuanBaquero99/ssl-monitoring-automation`

### 3. Agregar PostgreSQL

1. En el dashboard de Railway: `+ Add Service`
2. Seleccionar `PostgreSQL`
3. Railway conectará automáticamente las variables de entorno

### 4. Configurar n8n

Una vez deployado:
1. Ir a la URL generada por Railway
2. Login: `admin` / `crecemos2024`
3. Importar workflows desde `/workflows/`

## 📁 Estructura del Proyecto

```
aut-crecemos/
├── scripts/
│   ├── verificar_ssl.py      # Verificación SSL
│   └── enviar_alertas.py     # Sistema de alertas
├── data/
│   └── clientes_ejemplo.json # Base de datos clientes
├── workflows/
│   └── ssl_monitoring.json   # Workflow n8n
├── Dockerfile               # Configuración Docker
├── railway.json            # Configuración Railway
└── .env.example           # Variables de entorno
```

## � Costos

- **Railway**: $5 USD/mes gratuitos (suficiente)
- **Gmail SMTP**: Gratuito
- **Total**: $0 USD/mes

## 📊 Monitoreo

El sistema verificará automáticamente:
- **Certificados SSL**: Estado y días hasta vencimiento
- **Proveedores de Hosting**: Detección automática
- **Alertas**: Emails automáticos según criticidad

### Estados SSL:
- 🟢 **Excelente**: +30 días
- 🟡 **Advertencia**: 7-30 días  
- 🔴 **Urgente**: 1-7 días
- 💀 **Vencido**: 0 días

---
*Desarrollado por CrecemosLab - Automatización 100% gratuita* 🚀
