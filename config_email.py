"""
🔧 CONFIGURACIÓN DE EMAIL PARA ALERTAS SSL
====================================

Instrucciones:
1. Ve a myaccount.google.com/security
2. Activa "Verificación en dos pasos"
3. Ve a "Contraseñas de aplicaciones"
4. Genera una nueva contraseña para "Aplicación personalizada"
5. Usa esa contraseña de 16 caracteres aquí abajo

"""

# 📧 TU EMAIL DE GMAIL (el que enviará las alertas)
EMAIL_REMITENTE = "desarrollo@crecemoslab.com"

# 🔑 CONTRASEÑA DE APLICACIÓN DE GMAIL (16 caracteres sin espacios)
EMAIL_PASSWORD = "qgog iqdl wgzo vwut"  # Ejemplo: "abcd efgh ijkl mnop"

# 📨 EMAIL DONDE QUIERES RECIBIR LAS ALERTAS (puede ser el mismo)
EMAIL_DESTINATARIO = "desarrollo@crecemoslab.com"

# 📋 LISTA DE EMAILS ADICIONALES PARA NOTIFICAR (opcional)
EMAILS_ADICIONALES = [
    "hola@crecemoslab.com",
    "valentina@crecemoslab.com"
]

# ⚙️ CONFIGURACIÓN AVANZADA (no cambiar)
SMTP_CONFIG = {
    'servidor': 'smtp.gmail.com',
    'puerto': 587,
    'usar_tls': True
}

print("✅ Configuración de email cargada")
