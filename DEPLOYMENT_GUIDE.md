# 🚀 Guía de Deployment en Railway (100% Gratis)

## ✅ Paso 1: Subir a GitHub

1. **Crear repositorio en GitHub**:
   - Ir a https://github.com/new
   - Nombre: `ssl-monitoring-automation`
   - Descripción: `Sistema automatizado de monitoreo SSL con n8n`
   - Público o Privado (tu elección)
   - ✅ Crear repositorio

2. **Conectar repositorio local**:
   ```bash
   git remote add origin https://github.com/TU_USUARIO/ssl-monitoring-automation.git
   git branch -M main
   git push -u origin main
   ```

## 🚂 Paso 2: Deploy en Railway

1. **Crear cuenta**:
   - Ir a https://railway.app
   - Sign up with GitHub
   - ✅ Conectar tu cuenta GitHub

2. **Crear nuevo proyecto**:
   - Click "New Project"
   - "Deploy from GitHub repo"
   - Seleccionar `ssl-monitoring-automation`
   - ✅ Railway detectará automáticamente el Dockerfile

3. **Agregar PostgreSQL**:
   - En tu proyecto Railway: `+ Add Service`
   - Seleccionar `PostgreSQL`
   - ✅ Railway conectará automáticamente las variables de entorno

4. **Configurar variables de entorno** (opcional):
   - Variables ya están configuradas en el Dockerfile
   - Puedes cambiar la contraseña en Settings > Environment

## 🎯 Paso 3: Acceso a n8n

1. **Obtener URL**:
   - Railway te dará una URL como: `https://tu-proyecto.up.railway.app`
   - ✅ Abrir en navegador

2. **Login inicial**:
   - Usuario: `admin`
   - Contraseña: `crecemos2024`
   - ✅ Cambiar contraseña después del primer login

3. **Importar workflow**:
   - Settings > Import/Export
   - Subir: `/workflows/ssl_monitoring.json`
   - ✅ Activar el workflow

## ⚙️ Paso 4: Configurar Gmail SMTP

1. **Generar App Password**:
   - Gmail > Gestionar cuenta Google
   - Seguridad > Verificación en 2 pasos
   - Contraseñas de aplicaciones > Generar
   - ✅ Copiar la contraseña generada

2. **Configurar en n8n**:
   - Credentials > Add Credential
   - Tipo: "SMTP"
   - Host: `smtp.gmail.com`
   - Puerto: `587`
   - Usuario: tu email
   - Contraseña: app password generada
   - ✅ Guardar como "Gmail SMTP CrecemosLab"

## 📊 Paso 5: Verificar funcionamiento

1. **Ejecutar workflow manualmente**:
   - Abrir workflow "SSL Monitoring Automation"
   - Click "Execute Workflow"
   - ✅ Verificar que no hay errores

2. **Revisar logs**:
   - Railway Dashboard > Logs
   - ✅ Verificar que n8n inició correctamente

3. **Programar ejecución**:
   - El workflow está configurado para ejecutarse diariamente a las 8:00 AM
   - ✅ Puedes cambiar el horario en el Schedule Trigger

## 💰 Costos

- **Railway**: $5 USD/mes GRATIS
- **Gmail SMTP**: GRATIS
- **PostgreSQL**: GRATIS (incluido en Railway)
- **Total**: $0 USD/mes ✅

## 🔧 Mantenimiento

- **Logs**: Revisar Railway Dashboard regularmente
- **Actualizaciones**: Git push para deploy automático
- **Monitoreo**: Railway notifica si hay problemas
- **Backups**: PostgreSQL se respalda automáticamente

## ❗ Troubleshooting

### Error de conexión a base de datos:
```
Revisar variables de entorno en Railway
Verificar que PostgreSQL esté activo
```

### n8n no inicia:
```
Revisar logs en Railway Dashboard
Verificar que el Dockerfile es correcto
```

### Scripts Python fallan:
```
SSH a Railway container: railway shell
Verificar que los archivos están en /data/scripts/
```

### Emails no se envían:
```
Verificar App Password de Gmail
Comprobar credenciales SMTP en n8n
```

## 📞 Soporte

Si tienes problemas:
1. 📧 desarrollo@crecemoslab.com
2. 📱 Revisar logs de Railway
3. 🔍 Verificar configuración n8n

---
🎉 **¡Listo! Tu sistema de monitoreo SSL está 100% automatizado y gratuito!** 🎉
