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

print("✅ Importaciones de email cargadas correctamente")

def configurar_email():
    """
    Configuración de Gmail SMTP - Lee desde config_email.py
    """
    try:
        # Importar configuración
        import sys
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        sys.path.append(project_dir)
        
        import config_email
        
        config = {
            'smtp_server': config_email.SMTP_CONFIG['servidor'],
            'smtp_port': config_email.SMTP_CONFIG['puerto'],
            'email_user': config_email.EMAIL_REMITENTE,
            'email_password': config_email.EMAIL_PASSWORD,
            'email_destinatario': config_email.EMAIL_DESTINATARIO,
            'emails_adicionales': config_email.EMAILS_ADICIONALES
        }
        
        return config
        
    except ImportError:
        print("⚠️ No se encontró config_email.py, usando configuración por defecto")
        config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email_user': 'tu-email@gmail.com',  # ← Cambiar por tu email
            'email_password': 'tu-app-password',  # ← Cambiar por tu contraseña de aplicación
            'email_destinatario': 'alertas@tuempresa.com',  # ← Email donde recibirás las alertas
            'emails_adicionales': []
        }
        return config

def crear_template_consolidado(alertas_pendientes, es_reporte_limpio=False):
    """
    Crea el template HTML para múltiples alertas (SSL, hosting, dominio) o reporte limpio
    """
    fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
    
    # Obtener ruta del logo
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    logo_path = os.path.join(project_dir, 'assets', 'Crecemos.png')
    
    # Header del email
    if es_reporte_limpio:
        header_color = "#28a745"  # Verde
        header_text = "✅ REPORTE LIMPIO - Todo al día"
        total_alertas = 0
    else:
        total_alertas = len(alertas_pendientes)
        # Contar urgencias
        urgentes = sum(1 for alerta in alertas_pendientes if alerta['dias_restantes'] <= 7)
        importantes = sum(1 for alerta in alertas_pendientes if 8 <= alerta['dias_restantes'] <= 15)
        recordatorios = sum(1 for alerta in alertas_pendientes if alerta['dias_restantes'] > 15)
        
        # Determinar color de header según la alerta más crítica
        dias_minimos = min(alerta['dias_restantes'] for alerta in alertas_pendientes)
        if dias_minimos <= 7:
            header_color = "#dc3545"  # Rojo
            header_text = "🚨 ALERTAS URGENTES"
        elif dias_minimos <= 15:
            header_color = "#fd7e14"  # Naranja
            header_text = "⚠️ ALERTAS IMPORTANTES"
        else:
            header_color = "#0d6efd"  # Azul
            header_text = "📋 RECORDATORIOS"
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Reporte Monitoreo - {total_alertas if not es_reporte_limpio else 'Todo al día'}</title>
    </head>
    <body style="font-family: Arial, sans-serif; margin: 20px; background-color: #f8f9fa;">
        <div style="max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            
            <!-- Logo de la empresa -->
            <div style="text-align: center; margin-bottom: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
                <img src="cid:logo" alt="Crecemos Lab Logo" style="max-height: 80px; margin-bottom: 10px;">
                <p style="margin: 5px 0; color: #666; font-size: 14px;">Sistema de Monitoreo de Infraestructura Web</p>
            </div>
            
            <h1 style="color: {header_color}; text-align: center; margin-bottom: 20px;">
                {header_text}
            </h1>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; text-align: center;">"""
    
    if es_reporte_limpio:
        html_template += f"""
                <h2 style="color: #333; margin-top: 0;">🎉 ¡Excelente! Todo está al día</h2>
                <p style="font-size: 18px; margin: 10px 0; color: #28a745;">
                    <strong>✅ No hay vencimientos próximos en los próximos 30 días</strong>
                </p>
                <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #28a745;">
                    <p style="margin: 5px 0; color: #155724;"><strong>📊 Estado del monitoreo:</strong></p>
                    <ul style="color: #155724; margin: 10px 0; text-align: left;">
                        <li>🔐 <strong>SSL:</strong> Todos los certificados tienen más de 30 días</li>
                        <li>🏠 <strong>Hosting:</strong> Todos los servicios están vigentes</li>
                        <li>🌐 <strong>Dominios:</strong> Todas las renovaciones al día</li>
                    </ul>
                </div>"""
    else:
        html_template += f"""
                <h2 style="color: #333; margin-top: 0;">📊 Resumen de Alertas</h2>
                <p style="font-size: 18px; margin: 10px 0;">
                    <strong>Total de servicios por vencer:</strong> 
                    <span style="color: {header_color}; font-weight: bold; font-size: 24px;">{total_alertas}</span>
                </p>
                <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 15px;">"""
        
        if 'urgentes' in locals() and urgentes > 0:
            html_template += f"""
                        <div style="background-color: #dc3545; color: white; padding: 10px 15px; border-radius: 5px; min-width: 100px;">
                            <strong>🚨 URGENTES</strong><br>
                            <span style="font-size: 20px;">{urgentes}</span>
                            <br><small>≤ 7 días</small>
                        </div>"""
        
        if 'importantes' in locals() and importantes > 0:
            html_template += f"""
                        <div style="background-color: #fd7e14; color: white; padding: 10px 15px; border-radius: 5px; min-width: 100px;">
                            <strong>⚠️ IMPORTANTES</strong><br>
                            <span style="font-size: 20px;">{importantes}</span>
                            <br><small>8-15 días</small>
                        </div>"""
        
        if 'recordatorios' in locals() and recordatorios > 0:
            html_template += f"""
                        <div style="background-color: #0d6efd; color: white; padding: 10px 15px; border-radius: 5px; min-width: 100px;">
                            <strong>📋 RECORDATORIOS</strong><br>
                            <span style="font-size: 20px;">{recordatorios}</span>
                            <br><small>16-30 días</small>
                        </div>"""
    
    html_template += """
                </div>
            </div>"""
    
    if not es_reporte_limpio:
        html_template += """
            <h3 style="color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px;">📋 Detalle de Vencimientos</h3>"""
        
        # Ordenar alertas por días restantes (más urgente primero)
        alertas_ordenadas = sorted(alertas_pendientes, key=lambda x: x['dias_restantes'])
        
        for i, alerta in enumerate(alertas_ordenadas, 1):
            cliente = alerta['cliente']
            alertas_cliente = alerta['alertas']
            dias_restantes = alerta['dias_restantes']
            
            # Determinar estilo según urgencia
            if dias_restantes <= 7:
                urgencia_texto = "🚨 URGENTE"
                border_color = "#dc3545"
                bg_color = "#f8d7da"
            elif dias_restantes <= 15:
                urgencia_texto = "⚠️ IMPORTANTE"
                border_color = "#fd7e14"
                bg_color = "#fff3cd"
            else:
                urgencia_texto = "📋 RECORDATORIO"
                border_color = "#0d6efd"
                bg_color = "#d1ecf1"
            
            html_template += f"""
                <div style="border-left: 4px solid {border_color}; background-color: {bg_color}; padding: 15px; margin-bottom: 15px; border-radius: 0 5px 5px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                        <div style="flex: 1; min-width: 300px;">
                            <h4 style="margin: 0 0 10px 0; color: #333;">
                                {i}. {cliente['nombre']}
                            </h4>
                            <p style="margin: 5px 0; color: #666;">
                                <strong>🌐 Dominio:</strong> {cliente['dominio']}
                            </p>"""
            
            # Mostrar cada tipo de alerta para este cliente
            for alert in alertas_cliente:
                icon = "🔐" if alert['tipo'] == 'SSL' else "🏠" if alert['tipo'] == 'HOSTING' else "🌐"
                html_template += f"""
                            <p style="margin: 5px 0; color: #666;">
                                <strong>{icon} {alert['tipo']}:</strong> Vence en {alert['dias_restantes']} días - {alert['fecha_vencimiento']}
                            </p>
                            <p style="margin: 5px 0; color: #666; font-size: 12px;">
                                {alert['info_adicional']}
                            </p>"""
            
            html_template += f"""
                        </div>
                        <div style="text-align: center; min-width: 120px;">
                            <div style="background-color: {border_color}; color: white; padding: 10px; border-radius: 5px; margin-bottom: 5px;">
                                <strong style="font-size: 18px;">{dias_restantes}</strong><br>
                                <small>días mínimos</small>
                            </div>
                            <small style="color: {border_color}; font-weight: bold;">{urgencia_texto}</small>
                        </div>
                    </div>
                </div>"""
    
    html_template += f"""
            <div style="background-color: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h4 style="color: #333; margin-top: 0;">🔧 Acciones Recomendadas:</h4>
                <ul style="color: #666; margin: 10px 0;">
                    <li>Verificar que la renovación automática esté habilitada</li>
                    <li>Contactar a los proveedores correspondientes si es necesario</li>
                    <li>Actualizar métodos de pago en las cuentas</li>
                    <li>Programar verificación post-renovación</li>
                    <li>Considerar migrar a servicios con renovación automática</li>
                </ul>
            </div>
            
            <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h4 style="color: #856404; margin-top: 0;">📎 Archivo Adjunto</h4>
                <p style="color: #856404; margin: 5px 0;">
                    <strong>📊 Reporte Completo:</strong> Revisa el archivo CSV adjunto para ver el estado completo de todos los clientes, incluyendo fechas exactas de vencimiento de dominios, hosting y SSL.
                </p>
                <p style="color: #856404; margin: 5px 0; font-size: 12px;">
                    📝 <em>El archivo incluye: Cliente, Dominio, Proveedor, Fechas de vencimiento, Días restantes y Notas.</em>
                </p>
            </div>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            
            <div style="text-align: center; color: #666; font-size: 12px;">
                <p style="margin: 5px 0;">
                    <strong>📧 Reporte generado automáticamente por Crecemos Lab</strong>
                </p>
                <p style="margin: 5px 0;">
                    📅 Fecha: {fecha_actual} | 🔍 Clientes monitoreados: 24 | ⚠️ Alertas: {total_alertas if not es_reporte_limpio else 0}
                </p>
                <p style="margin: 5px 0; font-style: italic;">
                    {'Próxima verificación: siguiente lunes' if not es_reporte_limpio else 'Estado: Monitoreo continuo activo ✅'}
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template
    
    if urgentes > 0:
        html_template += f"""
                    <div style="background-color: #dc3545; color: white; padding: 10px 15px; border-radius: 5px; min-width: 100px;">
                        <strong>🚨 URGENTES</strong><br>
                        <span style="font-size: 20px;">{urgentes}</span>
                        <br><small>≤ 7 días</small>
                    </div>"""
    
    if importantes > 0:
        html_template += f"""
                    <div style="background-color: #fd7e14; color: white; padding: 10px 15px; border-radius: 5px; min-width: 100px;">
                        <strong>⚠️ IMPORTANTES</strong><br>
                        <span style="font-size: 20px;">{importantes}</span>
                        <br><small>8-15 días</small>
                    </div>"""
    
    if recordatorios > 0:
        html_template += f"""
                    <div style="background-color: #0d6efd; color: white; padding: 10px 15px; border-radius: 5px; min-width: 100px;">
                        <strong>📋 RECORDATORIOS</strong><br>
                        <span style="font-size: 20px;">{recordatorios}</span>
                        <br><small>16-30 días</small>
                    </div>"""
    
    html_template += """
                </div>
            </div>
            
            <h3 style="color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px;">📋 Detalle de Certificados</h3>
    """
    
    # Ordenar alertas por días restantes (más urgente primero)
    alertas_ordenadas = sorted(alertas_pendientes, key=lambda x: x['dias_restantes'])
    
    for i, alerta in enumerate(alertas_ordenadas, 1):
        cliente = alerta['cliente']
        ssl_info = alerta['ssl_info']
        dias_restantes = ssl_info['dias_restantes']
        
        # Determinar estilo según urgencia
        if dias_restantes <= 7:
            urgencia_texto = "🚨 URGENTE"
            border_color = "#dc3545"
            bg_color = "#f8d7da"
        elif dias_restantes <= 15:
            urgencia_texto = "⚠️ IMPORTANTE"
            border_color = "#fd7e14"
            bg_color = "#fff3cd"
        else:
            urgencia_texto = "📋 RECORDATORIO"
            border_color = "#0d6efd"
            bg_color = "#d1ecf1"
        
        html_template += f"""
            <div style="border-left: 4px solid {border_color}; background-color: {bg_color}; padding: 15px; margin-bottom: 15px; border-radius: 0 5px 5px 0;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 300px;">
                        <h4 style="margin: 0 0 10px 0; color: #333;">
                            {i}. {cliente['nombre']}
                        </h4>
                        <p style="margin: 5px 0; color: #666;">
                            <strong>🌐 Dominio:</strong> {cliente['dominio']}
                        </p>
                        <p style="margin: 5px 0; color: #666;">
                            <strong>📅 Vence:</strong> {ssl_info.get('fecha_vencimiento', 'No especificado')}
                        </p>
                        <p style="margin: 5px 0; color: #666;">
                            <strong>🏢 Emisor:</strong> {ssl_info.get('emisor', 'No especificado')}
                        </p>
                    </div>
                    <div style="text-align: center; min-width: 120px;">
                        <div style="background-color: {border_color}; color: white; padding: 10px; border-radius: 5px; margin-bottom: 5px;">
                            <strong style="font-size: 18px;">{dias_restantes}</strong><br>
                            <small>días restantes</small>
                        </div>
                        <small style="color: {border_color}; font-weight: bold;">{urgencia_texto}</small>
                    </div>
                </div>
            </div>
        """
    
    html_template += f"""
            <div style="background-color: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h4 style="color: #333; margin-top: 0;">🔧 Acciones Recomendadas:</h4>
                <ul style="color: #666; margin: 10px 0;">
                    <li>Verificar que la renovación automática esté habilitada en cada dominio</li>
                    <li>Contactar a los proveedores de hosting si es necesario</li>
                    <li>Actualizar métodos de pago en las cuentas correspondientes</li>
                    <li>Programar verificación post-renovación</li>
                    <li>Considerar migrar a SSL automático (Let's Encrypt) donde sea posible</li>
                </ul>
            </div>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            
            <div style="text-align: center; color: #666; font-size: 12px;">
                <p style="margin: 5px 0;">
                    <strong>📧 Reporte generado automáticamente por Sistema de Monitoreo SSL</strong>
                </p>
                <p style="margin: 5px 0;">
                    📅 Fecha: {fecha_actual} | 🔍 Clientes analizados: 20 | ⚠️ Alertas: {total_alertas}
                </p>
                <p style="margin: 5px 0; font-style: italic;">
                    Próxima verificación programada para el siguiente lunes
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_template

def generar_reporte_completo():
    """
    Genera un archivo CSV con el reporte completo de todos los clientes
    """
    try:
        import csv
        import os
        from datetime import datetime
        
        # Obtener ruta correcta del archivo JSON
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        json_path = os.path.join(project_dir, 'data', 'clientes_ejemplo.json')
        
        # Leer archivo de clientes
        with open(json_path, 'r', encoding='utf-8') as archivo:
            clientes = json.load(archivo)
        
        # Crear archivo temporal CSV
        fecha_actual = datetime.now().strftime('%Y%m%d_%H%M')
        csv_path = os.path.join(project_dir, f'reporte_completo_{fecha_actual}.csv')
        
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            
            # Encabezados
            writer.writerow([
                'ID', 'Cliente', 'Dominio', 'Proveedor Hosting', 
                'Vence Dominio', 'Vence Hosting', 'Estado SSL',
                'Días Restantes Dominio', 'Días Restantes Hosting',
                'Activo', 'Notas'
            ])
            
            for cliente in clientes:
                if not cliente.get('activo', True):
                    continue
                
                # Calcular días restantes
                dias_dominio = verificar_fecha_vencimiento(cliente.get('fecha_vencimiento_dominio', ''))
                dias_hosting = verificar_fecha_vencimiento(cliente.get('fecha_vencimiento_hosting', ''))
                
                # Obtener SSL actual (sin imprimir detalles)
                try:
                    from verificar_ssl import obtener_info_ssl
                    ssl_info = obtener_info_ssl(cliente['dominio'])
                    estado_ssl = f"Vence en {ssl_info['dias_restantes']} días" if ssl_info else "No verificado"
                except:
                    estado_ssl = "No verificado"
                
                writer.writerow([
                    cliente.get('id', ''),
                    cliente.get('nombre', ''),
                    cliente.get('dominio', ''),
                    cliente.get('proveedor_hosting', ''),
                    cliente.get('fecha_vencimiento_dominio', ''),
                    cliente.get('fecha_vencimiento_hosting', ''),
                    estado_ssl,
                    dias_dominio if dias_dominio is not None else 'N/A',
                    dias_hosting if dias_hosting is not None else 'N/A',
                    'Sí' if cliente.get('activo', True) else 'No',
                    cliente.get('notas', '')
                ])
        
        print(f"📊 Reporte completo generado: {csv_path}")
        return csv_path
        
    except Exception as error:
        print(f"❌ Error al generar reporte: {error}")
        return None

def enviar_email_alerta(destinatario, asunto, contenido_html, incluir_reporte=True):
    """
    Envía un email de alerta usando Gmail SMTP con logo y reporte completo adjunto
    """
    try:
        config = configurar_email()
        
        # Crear mensaje
        mensaje = MIMEMultipart("related")
        mensaje["Subject"] = asunto
        mensaje["From"] = config['email_user']
        mensaje["To"] = destinatario
        
        # Crear parte alternativa para HTML
        msg_alternativo = MIMEMultipart("alternative")
        mensaje.attach(msg_alternativo)
        
        # Agregar contenido HTML
        parte_html = MIMEText(contenido_html, "html")
        msg_alternativo.attach(parte_html)
        
        # Agregar logo como adjunto embedded
        try:
            import os
            from email.mime.image import MIMEImage
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(script_dir)
            logo_path = os.path.join(project_dir, 'assets', 'Crecemos.png')
            
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as archivo_logo:
                    img = MIMEImage(archivo_logo.read())
                    img.add_header('Content-ID', '<logo>')
                    img.add_header('Content-Disposition', 'inline', filename='logo.png')
                    mensaje.attach(img)
        except Exception as e:
            print(f"⚠️ No se pudo adjuntar el logo: {e}")
        
        # Agregar reporte CSV como adjunto
        if incluir_reporte:
            try:
                from email.mime.application import MIMEApplication
                
                csv_path = generar_reporte_completo()
                if csv_path and os.path.exists(csv_path):
                    with open(csv_path, 'rb') as archivo_csv:
                        csv_adjunto = MIMEApplication(archivo_csv.read(), _subtype='csv')
                        csv_adjunto.add_header(
                            'Content-Disposition', 
                            'attachment', 
                            filename=f'Reporte_Completo_Crecemos_{datetime.now().strftime("%d%m%Y")}.csv'
                        )
                        mensaje.attach(csv_adjunto)
                    
                    # Limpiar archivo temporal
                    try:
                        os.remove(csv_path)
                    except:
                        pass
                    
                    print("📎 Reporte CSV adjuntado al email")
            except Exception as e:
                print(f"⚠️ No se pudo adjuntar el reporte CSV: {e}")
        
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

def verificar_fecha_vencimiento(fecha_str):
    """
    Verifica una fecha de vencimiento y retorna días restantes
    """
    try:
        if fecha_str in ['Auto-renovable', 'Auto-verificar', 'Por determinar']:
            return None
        
        # Parsear diferentes formatos de fecha
        from datetime import datetime, timedelta
        fecha_hoy = datetime.now()
        
        # Intentar diferentes formatos
        formatos = ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']
        
        for formato in formatos:
            try:
                fecha_vencimiento = datetime.strptime(fecha_str, formato)
                dias_restantes = (fecha_vencimiento - fecha_hoy).days
                return dias_restantes
            except ValueError:
                continue
        
        return None
    except Exception:
        return None

def detectar_vencimientos_proximos():
    """
    Lee el archivo de clientes y detecta vencimientos próximos de SSL, hosting y dominios
    """
    try:
        # Importar función de verificar SSL
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from verificar_ssl import obtener_info_ssl
        
        # Obtener ruta correcta del archivo JSON
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        json_path = os.path.join(project_dir, 'data', 'clientes_ejemplo.json')
        
        # Leer archivo de clientes
        with open(json_path, 'r', encoding='utf-8') as archivo:
            clientes = json.load(archivo)
        
        alertas_pendientes = []
        
        print(f"🔍 Analizando {len(clientes)} clientes para detectar vencimientos...")
        
        for cliente in clientes:
            if not cliente.get('activo', True):
                continue
            
            cliente_alertas = []
            
            # 1. Verificar SSL real del cliente
            ssl_info = obtener_info_ssl(cliente['dominio'])
            if ssl_info and ssl_info['dias_restantes'] <= 30:
                cliente_alertas.append({
                    'tipo': 'SSL',
                    'dias_restantes': ssl_info['dias_restantes'],
                    'fecha_vencimiento': ssl_info.get('fecha_vencimiento', 'No especificado'),
                    'info_adicional': f"Emisor: {ssl_info.get('emisor', 'Desconocido')}"
                })
                print(f"⚠️ SSL: {cliente['nombre']} - SSL vence en {ssl_info['dias_restantes']} días")
            
            # 2. Verificar fecha de vencimiento de hosting
            dias_hosting = verificar_fecha_vencimiento(cliente.get('fecha_vencimiento_hosting'))
            if dias_hosting is not None and dias_hosting <= 30:
                cliente_alertas.append({
                    'tipo': 'HOSTING',
                    'dias_restantes': dias_hosting,
                    'fecha_vencimiento': cliente.get('fecha_vencimiento_hosting'),
                    'info_adicional': f"Proveedor: {cliente.get('proveedor_hosting', 'Desconocido')}"
                })
                print(f"⚠️ HOSTING: {cliente['nombre']} - Hosting vence en {dias_hosting} días")
            
            # 3. Verificar fecha de vencimiento de dominio
            dias_dominio = verificar_fecha_vencimiento(cliente.get('fecha_vencimiento_dominio'))
            if dias_dominio is not None and dias_dominio <= 30:
                cliente_alertas.append({
                    'tipo': 'DOMINIO',
                    'dias_restantes': dias_dominio,
                    'fecha_vencimiento': cliente.get('fecha_vencimiento_dominio'),
                    'info_adicional': f"Proveedor: {cliente.get('proveedor_hosting', 'Desconocido')}"
                })
                print(f"⚠️ DOMINIO: {cliente['nombre']} - Dominio vence en {dias_dominio} días")
            
            # Si hay alertas para este cliente, agregarlo
            if cliente_alertas:
                alerta = {
                    'cliente': cliente,
                    'ssl_info': ssl_info,
                    'alertas': cliente_alertas,
                    'dias_restantes': min(alert['dias_restantes'] for alert in cliente_alertas)
                }
                alertas_pendientes.append(alerta)
        
        return alertas_pendientes
        
    except Exception as error:
        print(f"❌ Error al detectar vencimientos: {error}")
        return []

def procesar_alertas():
    """
    Función principal que detecta vencimientos y envía UN SOLO email consolidado
    """
    print("🚨 === SISTEMA DE MONITOREO INTEGRAL ===")
    config = configurar_email()
    
    # Detectar vencimientos próximos
    alertas = detectar_vencimientos_proximos()
    
    if not alertas:
        print("🎉 ¡Excelente! No hay vencimientos próximos en los próximos 30 días.")
        print("📧 Enviando reporte de estado 'Todo al día'...")
        
        # Crear email de "todo al día" con logo
        contenido_html = crear_template_consolidado([], es_reporte_limpio=True)
        asunto = "✅ REPORTE LIMPIO - Todo al día | Monitoreo Crecemos Lab"
        
        # Enviar email principal (a ti)
        enviado_admin = enviar_email_alerta(
            config['email_destinatario'], 
            asunto, 
            contenido_html
        )
        
        # Enviar a emails adicionales
        for email_adicional in config.get('emails_adicionales', []):
            enviar_email_alerta(email_adicional, asunto, contenido_html)
            print(f"📧 Reporte enviado a: {email_adicional}")
        
        if enviado_admin:
            print("✅ Reporte 'Todo al día' enviado exitosamente")
        else:
            print("❌ Error al enviar reporte")
        
        print("📊 Proceso completado: Reporte de estado limpio enviado")
        return
    
    print(f"\n📧 Preparando email consolidado con {len(alertas)} alertas...")
    
    # Crear contenido HTML consolidado
    contenido_html = crear_template_consolidado(alertas, es_reporte_limpio=False)
    
    # Crear asunto dinámico
    total_alertas = len(alertas)
    dias_minimos = min(alerta['ssl_info']['dias_restantes'] for alerta in alertas)
    
    if dias_minimos <= 7:
        asunto = f"🚨 URGENTE: {total_alertas} certificados SSL por vencer (mínimo {dias_minimos} días)"
    elif dias_minimos <= 15:
        asunto = f"⚠️ IMPORTANTE: {total_alertas} certificados SSL por vencer (mínimo {dias_minimos} días)"
    else:
        asunto = f"� RECORDATORIO: {total_alertas} certificados SSL por vencer (mínimo {dias_minimos} días)"
    
    # Enviar email principal (a ti)
    enviado_admin = enviar_email_alerta(
        config['email_destinatario'], 
        asunto, 
        contenido_html
    )
    
    # Enviar a emails adicionales
    for email_adicional in config.get('emails_adicionales', []):
        enviar_email_alerta(email_adicional, asunto, contenido_html)
        print(f"📧 Copia enviada a: {email_adicional}")
    
    if enviado_admin:
        print(f"✅ Email consolidado enviado con {total_alertas} alertas")
        # Mostrar resumen en consola
        print("\n📋 Clientes incluidos en la alerta:")
        for i, alerta in enumerate(alertas, 1):
            cliente = alerta['cliente']
            dias = alerta['ssl_info']['dias_restantes']
            print(f"   {i}. {cliente['nombre']} - {dias} días restantes")
    else:
        print("❌ Error al enviar email consolidado")
    
    print(f"\n📊 Proceso completado: 1 email enviado con {len(alertas)} alertas")

if __name__ == "__main__":
    print("🧪 Probando sistema de alertas por email...")
    procesar_alertas()
