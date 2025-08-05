<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Instrucciones para GitHub Copilot - Proyecto de Monitoreo de Clientes

## Contexto del Proyecto
Este es un sistema de automatización para monitorear 21 clientes, incluyendo:
- Vencimientos de dominios
- Vencimientos de hosting
- Vencimientos de certificados SSL
- Monitoreo de caídas de sitios web
- Alertas preventivas por email

## Tecnologías Principales
- **n8n** para automatización de workflows
- **Python** para scripts de monitoreo
- **PostgreSQL** (Supabase) para base de datos
- **Gmail SMTP** para alertas
- **Railway/Render** para deployment gratuito

## Estilo de Código
- Usar Python 3.8+ con type hints
- Logging detallado con loguru
- Manejo robusto de errores
- Configuración a través de variables de entorno
- Documentación clara en español

## Estructura de Datos
- Cada cliente tiene: nombre, dominio, fecha_vencimiento_dominio, fecha_vencimiento_hosting, fecha_vencimiento_ssl
- Usar dataclasses o Pydantic para modelos
- Fechas en formato ISO 8601

## Convenciones
- Nombres de archivos en snake_case
- Funciones descriptivas en español
- Comentarios en español
- Variables de configuración en mayúsculas
- Logs informativos y de error detallados
