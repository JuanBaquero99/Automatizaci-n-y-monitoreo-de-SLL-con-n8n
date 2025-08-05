"""
Script para verificar certificados SSL de sitios web
Este script nos ayuda a monitorear cuándo vencen los certificados SSL
"""

import ssl          # Para obtener información de certificados SSL
import socket       # Para conectarse a servidores web
from datetime import datetime, timezone  # Para trabajar con fechas
import sys          # Para salir del programa si hay errores

# Esta librería la instalaremos después con pip
# from loguru import logger  # Para mostrar mensajes bonitos (comentada por ahora)

print("Importaciones cargadas correctamente")

def obtener_info_ssl(dominio):
    """
    Esta función obtiene información del certificado SSL de un dominio.
    """
    try:
        print(f"Obteniendo información SSL de {dominio}...")
        
        #Conectarse y obtener el certificado SSL usando un protocolo fuerte
        context = ssl.create_default_context()
        
        # Forzar el uso de TLSv1.2 como mínimo para mayor seguridad
        if hasattr(ssl, "TLSVersion"):
            context.minimum_version = ssl.TLSVersion.TLSv1_2
        else:
            context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        with socket.create_connection((dominio, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=dominio) as ssock:
                cert_info = ssock.getpeercert()
        
        # Extraer la fecha de vencimiento del certificado        print(f"SSL válido hasta: {fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S')}")        print(f"SSL válido hasta: {fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S')}")
        fecha_vencimiento_str = cert_info['notAfter']
        fecha_vencimiento = datetime.strptime(fecha_vencimiento_str, '%b %d %H:%M:%S %Y %Z')
        
        # Calcular los días restantes hasta el vencimiento
        hoy = datetime.now()
        dias_restantes = (fecha_vencimiento - hoy).days
        
        # Determinar el estado según días restantes
        if dias_restantes > 30:
            estado = "🟢 EXCELENTE"
            color_emoji = "✅"
        elif dias_restantes > 7:
            estado = "🟡 ADVERTENCIA"
            color_emoji = "⚠️"
        elif dias_restantes > 0:
            estado = "🔴 URGENTE"
            color_emoji = "🚨"
        else:
            estado = "💀 VENCIDO"
            color_emoji = "❌"
        
        # Obtener información adicional del certificado
        emisor = cert_info.get('issuer', [])
        emisor_nombre = ""
        for item in emisor:
            if item[0][0] == 'organizationName':
                emisor_nombre = item[0][1]
                break
        
        # Detectar si es Let's Encrypt (gratuito) o pagado
        es_lets_encrypt = "Let's Encrypt" in emisor_nombre
        tipo_ssl = "🆓 Gratuito (Let's Encrypt)" if es_lets_encrypt else "💳 Pagado/Comercial"
        
        # Detectar proveedor de hosting
        hosting_info = detectar_proveedor_hosting(dominio)
        
        # Mostrar información mejorada
        print(f"\n{color_emoji} === REPORTE SSL DE {dominio.upper()} ===")
        print(f"📅 Vence: {fecha_vencimiento.strftime('%d/%m/%Y a las %H:%M')}")
        print(f"⏰ Días restantes: {dias_restantes}")
        print(f"🏢 Emisor SSL: {emisor_nombre}")
        print(f"🔐 Tipo SSL: {tipo_ssl}")
        print(f"🌐 Proveedor: {hosting_info['proveedor']}")
        print(f"⚙️ Servidor: {hosting_info['servidor_web']}")
        if hosting_info['tecnologia'] != 'Desconocido':
            print(f"💻 Tecnología: {hosting_info['tecnologia']}")
        if hosting_info['cdn']:
            print(f"🚀 CDN: {hosting_info['cdn']}")
        print(f"📊 Estado: {estado}")
        print("=" * 50)
        return {
            'dominio': dominio,
            'fecha_vencimiento': fecha_vencimiento,
            'dias_restantes': dias_restantes,
            'valido': dias_restantes > 0,
            'emisor': emisor_nombre,
            'tipo_ssl': tipo_ssl,
            'estado': estado,
            'proveedor_hosting': hosting_info['proveedor'],
            'servidor_web': hosting_info['servidor_web'],
            'tecnologia': hosting_info['tecnologia'],
            'cdn': hosting_info['cdn']
        }
    except Exception as error:
        print(f"Error al obtener información SSL de {dominio}: {error}")
        return None

def detectar_proveedor_hosting(dominio):
    """
    Detecta el proveedor de hosting analizando headers HTTP y otros indicadores
    """
    import requests
    import subprocess
    
    proveedor_info = {
        'proveedor': 'Desconocido',
        'servidor_web': 'Desconocido',
        'tecnologia': 'Desconocido',
        'cdn': None
    }
    
    try:
        # Paso 1: Obtener headers HTTP
        print(f"🔍 Analizando hosting de {dominio}...")
        response = requests.get(f"https://{dominio}", timeout=10, allow_redirects=True)
        headers = response.headers
        
        # Paso 2: Detectar servidor web
        servidor = headers.get('Server', '').lower()
        if 'nginx' in servidor:
            proveedor_info['servidor_web'] = 'Nginx'
        elif 'apache' in servidor:
            proveedor_info['servidor_web'] = 'Apache'
        elif 'cloudflare' in servidor:
            proveedor_info['servidor_web'] = 'Cloudflare'
            proveedor_info['cdn'] = 'Cloudflare'
        elif 'microsoft' in servidor or 'iis' in servidor:
            proveedor_info['servidor_web'] = 'Microsoft IIS'
        
        # Paso 3: Detectar proveedores por headers específicos
        if 'hostinger' in servidor or 'hostinger' in str(headers).lower():
            proveedor_info['proveedor'] = 'Hostinger'
        elif 'godaddy' in str(headers).lower():
            proveedor_info['proveedor'] = 'GoDaddy'
        elif 'cloudflare' in str(headers).lower():
            proveedor_info['proveedor'] = 'Cloudflare'
        elif 'aws' in str(headers).lower() or 'amazon' in str(headers).lower():
            proveedor_info['proveedor'] = 'Amazon AWS'
        elif 'google' in str(headers).lower():
            proveedor_info['proveedor'] = 'Google Cloud'
        
        # Paso 4: Detectar tecnologías adicionales
        if 'wordpress' in str(headers).lower():
            proveedor_info['tecnologia'] = 'WordPress'
        elif 'wix' in str(headers).lower():
            proveedor_info['proveedor'] = 'Wix'
            proveedor_info['tecnologia'] = 'Wix'
        
        return proveedor_info
        
    except Exception as error:
        print(f"⚠️ No se pudo detectar el proveedor de {dominio}: {error}")
        return proveedor_info

def verificar_todos_los_clientes():
    """
    Lee el archivo JSON y verifica SSL de todos los clientes
    """
    import json
    
    try:
        # Leer archivo de clientes
        with open('data/clientes_ejemplo.json', 'r', encoding='utf-8') as archivo:
            clientes = json.load(archivo)
        
        print(f"🔍 Verificando SSL de {len(clientes)} clientes...\n")
        
        resultados = []
        for cliente in clientes:
            if cliente.get('activo', True):  # Solo clientes activos
                resultado = obtener_info_ssl(cliente['dominio'])
                if resultado:
                    resultado['nombre_cliente'] = cliente['nombre']
                    resultado['email_contacto'] = cliente['email_contacto']
                    resultados.append(resultado)
                    
        return resultados
        
    except FileNotFoundError:
        print("❌ No se encontró el archivo de clientes")
        return []
    except Exception as error:
        print(f"❌ Error al leer clientes: {error}")
        return []

if __name__ == "__main__":
    print("🧪 Probando detección de proveedor con un dominio...")
    
    # Probar solo con un dominio para ver la nueva funcionalidad
    resultado = obtener_info_ssl("lacarolinamedical.com")
    
    if resultado:
        print(f"\n✅ Prueba exitosa!")
        print(f"Proveedor detectado: {resultado['proveedor_hosting']}")
        print(f"Servidor web: {resultado['servidor_web']}")
    else:
        print("❌ No se pudo verificar el dominio")