# 🚀 Sistema Manual de Monitoreo SSL

Sistema ultra-ligero para verificar certificados SSL **manualmente** cada lunes.

## 🎯 Uso Simple

**Windows:**
```cmd
ejecutar_monitoreo.bat
```

**Linux/Mac:**
```bash
./ejecutar_monitoreo.sh
```

## 📊 Qué hace

- ✅ Verifica 20 clientes SSL automáticamente
- ✅ Detecta vencimientos próximos (≤ 30 días)  
- ✅ Envía alertas por email cuando es necesario
- ✅ Funciona 100% local, sin servidores

## 💾 Súper Ligero

**Total**: ~15 KB
- Scripts Python: ~10 KB
- Base de datos: ~2 KB
- Ejecutables: ~1 KB
- Docs: ~2 KB

## 📧 Gmail (Opcional)

Para alertas automáticas:
```bash
set EMAIL_USER=tu-email@gmail.com
set EMAIL_PASSWORD=tu-app-password
set EMAIL_DESTINATARIO=alertas@empresa.com
```

## 🗓️ Rutina Semanal

- **Frecuencia**: Cada lunes (o cuando quieras)
- **Tiempo**: 2-3 minutos
- **Costo**: $0

---
*Versión manual ultra-ligera - Solo Python, sin servidores* 🎯
