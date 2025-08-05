# n8n Automation Server
FROM n8nio/n8n:1.45.1

# Variables de entorno para configuración
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=crecemos2024
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=https
ENV NODE_ENV=production
ENV WEBHOOK_URL=https://n8n-production.up.railway.app/

# Configurar timezone
ENV GENERIC_TIMEZONE=America/Bogota
ENV TZ=America/Bogota

# Copiar nuestros scripts de Python al contenedor
COPY scripts/ /data/scripts/
COPY data/ /data/data/

# Exponer puerto
EXPOSE 5678

# Comando de inicio
CMD ["n8n", "start"]
