"""
Keep-alive script para mantener n8n activo en Render
Hace ping cada 10 minutos para evitar hibernación
"""

import requests
import time
import os
from datetime import datetime

def mantener_activo():
    """
    Hace ping al servidor cada 10 minutos
    """
    # URL de tu aplicación en Render (actualizar cuando tengas la URL)
    url = os.getenv('RENDER_URL', 'https://ssl-monitoring.onrender.com')
    
    while True:
        try:
            print(f"🏓 Ping a {url} - {datetime.now()}")
            response = requests.get(f"{url}/healthz", timeout=30)
            print(f"✅ Respuesta: {response.status_code}")
            
        except Exception as error:
            print(f"❌ Error en ping: {error}")
        
        # Esperar 10 minutos (600 segundos)
        time.sleep(600)

if __name__ == "__main__":
    print("🚀 Iniciando keep-alive para n8n...")
    mantener_activo()
