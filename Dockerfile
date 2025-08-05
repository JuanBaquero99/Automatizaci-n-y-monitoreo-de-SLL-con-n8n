# Solución definitiva ultra-minimalista
FROM n8nio/n8n:1.45.1

USER root

# Solo lo esencial
RUN apk add --no-cache python3 py3-requests

# Copiar scripts
COPY scripts/ /data/scripts/
COPY data/ /data/data/
COPY workflows/ /data/workflows/

# Permisos básicos
RUN chown -R node:node /data

USER node

# Solo variables críticas
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
ENV N8N_BASIC_AUTH_PASSWORD=crecemos2024
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678

EXPOSE 5678

# Usar el comando exacto de la imagen oficial
CMD ["tini", "--", "/usr/local/bin/n8n", "start"]
