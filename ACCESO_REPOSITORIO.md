# 🤝 Instrucciones para Dar Acceso al Repositorio

## Opción 1: Agregar como Colaborador (Recomendado)

### Para el dueño del repositorio (JuanBaquero99):

1. **Ir al repositorio en GitHub**:
   ```
   https://github.com/JuanBaquero99/Automatizaci-n-y-monitoreo-de-SLL-con-n8n
   ```

2. **Navegar a Settings**:
   - Click en la pestaña "Settings" del repositorio
   - Scroll down hasta "Collaborators and teams"

3. **Agregar colaborador**:
   - Click "Add people"
   - Ingresar el username de GitHub del colaborador
   - Seleccionar permisos: "Write" (suficiente para deploy)
   - Click "Add [username] to this repository"

4. **Confirmación**:
   - El colaborador recibirá un email de invitación
   - Debe aceptar la invitación para acceder

### Para el colaborador:

1. **Revisar email** de GitHub con la invitación
2. **Click "Accept invitation"**
3. **Verificar acceso** al repositorio
4. **Proceder con deploy** usando `GUIA_COLABORADOR.md`

---

## Opción 2: Fork del Repositorio (Alternativa)

### Para el colaborador:

1. **Ir al repositorio**:
   ```
   https://github.com/JuanBaquero99/Automatizaci-n-y-monitoreo-de-SLL-con-n8n
   ```

2. **Hacer Fork**:
   - Click en "Fork" (esquina superior derecha)
   - Seleccionar tu cuenta personal
   - Click "Create fork"

3. **Usar tu fork para deploy**:
   - En Railway, usar tu repositorio: `TuUsername/Automatizaci-n-y-monitoreo-de-SLL-con-n8n`
   - Seguir la `GUIA_COLABORADOR.md` normalmente

---

## ✅ Verificación de Acceso

El colaborador debe poder ver:
- ✅ El código fuente completo
- ✅ Todos los archivos (scripts/, workflows/, etc.)
- ✅ El historial de commits
- ✅ Issues y Pull Requests (si aplica)

---

## 📧 Información de Contacto

**Para coordinar el deploy**:
- Repositorio: `JuanBaquero99/Automatizaci-n-y-monitoreo-de-SLL-con-n8n`
- Contacto: desarrollo@crecemoslab.com
- Documentación: `GUIA_COLABORADOR.md`

**Una vez completado el deploy**:
- Compartir la URL de Railway generada
- Confirmar que n8n está accesible
- Verificar que el workflow se puede activar

---

🎯 **Objetivo**: Tener el sistema funcionando en Railway con monitoreo 24/7 de certificados SSL para los 20 clientes.
