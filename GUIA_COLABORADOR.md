# 🚀 Guía de Deploy para Colaborador - Railway

Esta guía es para que puedas deployar el sistema de monitoreo SSL en Railway usando tu propia cuenta.

## 📋 Requisitos previos
- ✅ Acceso al repositorio: `JuanBaquero99/Automatizaci-n-y-monitoreo-de-SLL-con-n8n`
- ✅ Cuenta de GitHub activa
- ✅ Cuenta de Gmail para alertas (opcional por ahora)

## 🚂 Paso 1: Crear cuenta en Railway

1. **Ir a**: https://railway.app
2. **Click**: "Start a New Project"
3. **Seleccionar**: "Login with GitHub"
4. **Autorizar**: Railway para acceder a repositorios
5. ✅ **Confirmar**: Que puedes ver repositorios compartidos

## 🔗 Paso 2: Deploy desde GitHub

1. **En Railway Dashboard**: Click "New Project"
2. **Seleccionar**: "Deploy from GitHub repo"
3. **Buscar**: `JuanBaquero99/Automatizaci-n-y-monitoreo-de-SLL-con-n8n`
4. **Click**: En el repositorio para deployar
5. ✅ **Railway detectará**: El Dockerfile automáticamente

## 🗄️ Paso 3: Agregar PostgreSQL

1. **En tu proyecto**: Click "+ Add Service"
2. **Seleccionar**: "PostgreSQL"
3. **Confirmar**: La creación de la base de datos
4. ✅ **Railway conectará**: Las variables automáticamente

## ⚙️ Paso 4: Configurar variables (opcional)

Si quieres cambiar credenciales:
1. **Ir a**: Settings > Environment
2. **Variables disponibles**:
   - `N8N_BASIC_AUTH_USER` (default: admin)
   - `N8N_BASIC_AUTH_PASSWORD` (default: crecemos2024)
   - `GENERIC_TIMEZONE` (default: America/Bogota)

## ⏰ Paso 5: Esperar el deploy

1. **Ver logs**: En tiempo real durante la construcción
2. **Tiempo estimado**: 3-5 minutos
3. **Indicador**: ✅ Verde cuando esté listo
4. **URL generada**: Algo como `https://ssl-monitoring-xxx.up.railway.app`

## 🎯 Paso 6: Acceder a n8n

1. **Abrir**: La URL generada por Railway
2. **Login**:
   - Usuario: `admin`
   - Contraseña: `crecemos2024`
3. ✅ **Confirmar**: Que n8n carga correctamente

## 📊 Paso 7: Importar workflow

1. **En n8n**: Settings > Import/Export
2. **Copy/paste** este JSON:

```json
{
  "name": "SSL Monitoring - Weekly Monday Check",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "cronExpression",
              "expression": "0 9 * * 1"
            }
          ]
        }
      },
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "name": "Weekly SSL Check - Mondays 9AM",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "command": "python /data/scripts/verificar_ssl.py",
        "options": {}
      },
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d480",
      "name": "Run SSL Check",
      "type": "n8n-nodes-base.executeCommand",
      "typeVersion": 1,
      "position": [460, 300]
    }
  ],
  "connections": {
    "Weekly SSL Check - Mondays 9AM": {
      "main": [
        [
          {
            "node": "Run SSL Check",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

3. **Click**: Import
4. ✅ **Activar**: El workflow

## 📧 Paso 8: Configurar Gmail (opcional)

Si quieres configurar alertas por email:

1. **Generar App Password en Gmail**:
   - Gmail > Gestionar cuenta > Seguridad
   - Verificación en 2 pasos > Contraseñas de aplicaciones
   - Generar nueva contraseña

2. **En n8n**:
   - Credentials > Add Credential
   - Tipo: "SMTP"
   - Host: `smtp.gmail.com`
   - Puerto: `587`
   - Usuario: tu email
   - Contraseña: app password generada

## ✅ Verificación final

1. **Probar workflow**: Execute Workflow manualmente
2. **Revisar logs**: En Railway Dashboard
3. **Confirmar**: Que los scripts Python funcionan
4. **Verificar**: Que PostgreSQL está conectado

## 💰 Costos

- **Railway**: $5 USD/mes GRATUITOS (suficiente para este proyecto)
- **PostgreSQL**: Incluido gratis en Railway
- **n8n**: Self-hosted gratis
- **Total**: $0 USD/mes

## 🔧 Troubleshooting

### Error "Repository not found":
- Verificar que tienes acceso al repo
- Confirmar que estás logueado en GitHub

### Error de construcción Docker:
- Revisar logs en Railway
- Verificar que el Dockerfile está presente

### n8n no carga:
- Esperar 5 minutos después del deploy
- Revisar logs de Railway
- Verificar que el puerto 5678 está expuesto

### Scripts Python fallan:
- Verificar que las dependencias se instalaron
- Revisar logs de ejecución en n8n

## 📞 Soporte

Si tienes problemas:
1. 📧 Contactar a: desarrollo@crecemoslab.com
2. 📱 Revisar logs de Railway Dashboard
3. 🔍 Verificar variables de entorno

---
🎉 **¡Listo! Tu sistema de monitoreo SSL está funcionando 24/7!** 🎉

**Características activas**:
- ✅ Monitoreo de 20 clientes
- ✅ Verificación diaria automática  
- ✅ Base de datos PostgreSQL
- ✅ Dashboard n8n completo
- ✅ Logs de auditoría
- ✅ 100% gratuito
