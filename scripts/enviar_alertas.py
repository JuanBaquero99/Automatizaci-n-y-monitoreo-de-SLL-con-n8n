"""
Script para enviar alertas por email sobre vencimientos
Envía emails automáticos cuando SSL, hosting o dominios están por vencer
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('config/.env')

print("✅ Importaciones de email cargadas correctamente")

def configurar_email():
    """
    Configuración de Gmail SMTP
    """
    config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'email_user': os.getenv('EMAIL_USER', 'tu-email@gmail.com'),
        'email_password': os.getenv('EMAIL_PASSWORD', 'tu-app-password'),
        'email_destinatario': os.getenv('EMAIL_DESTINATARIO', 'alertas@tuempresa.com')
    }
    
    return config

def crear_template_ssl_alerta(cliente_info, dias_restantes):
    """
    Crea el template HTML para alertas de SSL
    """
    # Determinar urgencia
    if dias_restantes <= 7:
        urgencia = "🚨 URGENTE"
        color = "#dc3545"  # Rojo
    elif dias_restantes <= 15:
        urgencia = "⚠️ IMPORTANTE"
        color = "#fd7e14"  # Naranja
    else:
        urgencia = "📋 RECORDATORIO"
        color = "#0d6efd"  # Azul
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Alerta SSL - {cliente_info['nombre']}</title>
    </head>
    <body style="font-family: Arial, sans-serif; margin: 20px; background-color: #f8f9fa;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            
            <h1 style="color: {color}; text-align: center; margin-bottom: 20px;">
                {urgencia}: Vencimiento SSL
            </h1>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <h2 style="color: #333; margin-top: 0;">Cliente: {cliente_info['nombre']}</h2>
                <p><strong>Dominio:</strong> {cliente_info['dominio']}</p>
                <p><strong>Días restantes:</strong> <span style="color: {color}; font-weight: bold;">{dias_restantes} días</span></p>
                <p><strong>Vence el:</strong> {cliente_info.get('fecha_vencimiento_ssl', 'No especificado')}</p>
            </div>
            
            <div style="margin-bottom: 20px;">
                <h3 style="color: #333;">Acciones recomendadas:</h3>
                <ul style="color: #666;">
                    <li>Verificar que la renovación automática esté habilitada</li>
                    <li>Contactar al proveedor de hosting si es necesario</li>
                    <li>Actualizar métodos de pago si aplica</li>
                    <li>Programar verificación post-renovación</li>
                </ul>
            </div>
            
            <div style="background-color: #e7f3ff; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p style="margin: 0; color: #333;">
                    <strong>Contacto del cliente:</strong> {cliente_info.get('email_contacto', 'No especificado')}
                </p>
            </div>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            
            <p style="color: #666; font-size: 12px; text-align: center;">
                Alerta generada automáticamente por Sistema de Monitoreo de Clientes<br>
                Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            </p>
        </div>
    </body>
    </html>
    """
    
    return html_template

def enviar_email_alerta(destinatario, asunto, contenido_html):
    """
    Envía un email de alerta usando Gmail SMTP
    """
    try:
        config = configurar_email()
        
        # Crear mensaje
        mensaje = MIMEMultipart("alternative")
        mensaje["Subject"] = asunto
        mensaje["From"] = config['email_user']
        mensaje["To"] = destinatario
        
        # Agregar contenido HTML
        parte_html = MIMEText(contenido_html, "html")
        mensaje.attach(parte_html)
        
        # Conectar y enviar
        print(f"📧 Enviando email a {destinatario}...")
        
        context = ssl.create_default_context()
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as servidor:
            servidor.starttls(context=context)
            servidor.login(config['email_user'], config['email_password'])
            servidor.sendmail(config['email_user'], destinatario, mensaje.as_string())
        
        print(f"✅ Email enviado exitosamente a {destinatario}")
        return True
        
    except Exception as error:
        print(f"❌ Error al enviar email: {error}")
        return False

def detectar_vencimientos_proximos():
    """
    Lee el archivo de clientes y detecta vencimientos próximos usando SSL real
    """
    try:
        # Importar función de verificar SSL
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from verificar_ssl import obtener_info_ssl
        
        # Leer archivo de clientes
        with open('data/clientes_ejemplo.json', 'r', encoding='utf-8') as archivo:
            clientes = json.load(archivo)
        
        alertas_pendientes = []
        
        print(f"🔍 Analizando {len(clientes)} clientes para detectar vencimientos...")
        
        for cliente in clientes:
            if not cliente.get('activo', True):
                continue
                
            # Verificar SSL real del cliente
            ssl_info = obtener_info_ssl(cliente['dominio'])
            
            if ssl_info and ssl_info['dias_restantes'] <= 30:  # 30 días o menos
                alerta = {
                    'cliente': cliente,
                    'ssl_info': ssl_info,
                    'tipo_alerta': 'SSL',
                    'dias_restantes': ssl_info['dias_restantes']
                }
                alertas_pendientes.append(alerta)
                print(f"⚠️ Alerta: {cliente['nombre']} - SSL vence en {ssl_info['dias_restantes']} días")
        
        return alertas_pendientes
        
    except Exception as error:
        print(f"❌ Error al detectar vencimientos: {error}")
        return []

def procesar_alertas():
    """
    Función principal que detecta vencimientos y envía alertas
    """
    print("🚨 === SISTEMA DE ALERTAS AUTOMÁTICAS ===")
    config = configurar_email()
    
    # Detectar vencimientos próximos
    alertas = detectar_vencimientos_proximos()
    
    if not alertas:
        print("🎉 ¡No hay vencimientos próximos! Todos los SSL están en buen estado.")
        return
    
    print(f"\n📧 Enviando {len(alertas)} alertas...")
    
    for alerta in alertas:
        cliente = alerta['cliente']
        ssl_info = alerta['ssl_info']
        
        # Crear contenido del email
        contenido_html = crear_template_ssl_alerta(cliente, ssl_info['dias_restantes'])
        
        # Crear asunto
        asunto = f"🚨 ALERTA SSL: {cliente['nombre']} vence en {ssl_info['dias_restantes']} días"
        
        # Enviar email
        enviado = enviar_email_alerta(
            config['email_destinatario'], 
            asunto, 
            contenido_html
        )
        
        if enviado:
            print(f"✅ Alerta enviada para {cliente['nombre']}")
        else:
            print(f"❌ Error al enviar alerta para {cliente['nombre']}")
    
    print(f"\n📊 Proceso completado: {len(alertas)} alertas procesadas")

if __name__ == "__main__":
    print("🧪 Probando sistema de alertas por email...")
    procesar_alertas()
