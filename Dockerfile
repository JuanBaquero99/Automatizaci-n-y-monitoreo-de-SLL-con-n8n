# Solución definitiva - n8n con Node.js base
FROM node:18-alpine

# Instalar n8n globalmente y dependencias Python
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-requests \
    tzdata && \
    npm install -g n8n@1.45.1 && \
    pip3 install --break-system-packages \
    loguru \
    python-dateutil

# Crear usuario y directorios
RUN addgroup -g 1000 node && \
    adduser -u 1000 -G node -s /bin/sh -D node && \
    mkdir -p /data/scripts /data/data /data/workflows /home/node/.n8n && \
    chown -R node:node /data /home/node/.n8n

# Copiar archivos como root
COPY scripts/ /data/scripts/
COPY data/ /data/data/
COPY workflows/ /data/workflows/

# Configurar permisos
RUN chmod +x /data/scripts/*.py && \
    chown -R node:node /data /home/node/.n8n

# Cambiar a usuario node
USER node
WORKDIR /home/node

# Variables de entorno
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=crecemos2024
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_USER_FOLDER=/home/node/.n8n
ENV GENERIC_TIMEZONE=America/Bogota

# Puerto
EXPOSE 5678

# Comando definitivo
CMD ["n8n", "start"]
