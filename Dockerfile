# n8n Automation Server with Python support
FROM n8nio/n8n:1.45.1

# Cambiar a root para instalar dependencias
USER root

# Instalar Python y dependencias en una sola capa
RUN apk add --no-cache \
    gcc \
    libffi-dev \
    musl-dev \
    openssl-dev \
    py3-pip \
    python3 \
    python3-dev \
    tzdata && \
    pip3 install --break-system-packages --no-cache-dir \
    loguru \
    python-dateutil \
    requests

# Crear directorios y configurar permisos
RUN mkdir -p /data/scripts /data/data /data/workflows /home/node/.n8n && \
    chown -R node:node /data /home/node/.n8n

# Copiar archivos
COPY scripts/ /data/scripts/
COPY data/ /data/data/
COPY workflows/ /data/workflows/

# Configurar permisos de ejecución
RUN chmod +x /data/scripts/*.py && \
    chown -R node:node /data /home/node/.n8n

# Cambiar de vuelta al usuario node
USER node

# Variables de entorno para configuración
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=crecemos2024
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV NODE_ENV=production
ENV GENERIC_TIMEZONE=America/Bogota
ENV TZ=America/Bogota
ENV N8N_USER_FOLDER=/home/node/.n8n

# Exponer puerto
EXPOSE 5678

# Comando de inicio directo sin script
CMD ["n8n", "start"]
