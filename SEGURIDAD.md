# 🔐 GUÍA DE SEGURIDAD - DELIZZIA POS

## ⚠️ PROBLEMAS CRÍTICOS IDENTIFICADOS Y CORREGIDOS

### 🚨 **EL SECRET_KEY ES CRÍTICO PARA LA SEGURIDAD**

**¿Qué hace el SECRET_KEY?**
- **Firma tokens JWT** que autentican a todos los usuarios
- **Verifica tokens JWT** en cada request al sistema
- **¡Si alguien conoce esta clave, puede hacerse pasar por cualquier usuario!**

### ✅ **CORRECCIONES IMPLEMENTADAS:**

1. **🔑 SECRET_KEY Seguro Generado**
   - Generado con `secrets.token_urlsafe(32)` 
   - Único e impredecible
   - Reemplazado en todos los archivos

2. **🗄️ SQL Logging Desactivado**
   - Evita leak de datos sensibles en logs
   - Configurable via `SQL_ECHO=false`

3. **👤 Script de Admin Seguro**
   - `backend/scripts/create_admin.py`
   - Genera contraseñas seguras automáticamente
   - Validación de fortaleza de contraseña

4. **📁 Variables de Entorno Separadas**
   - `.env.example` con plantilla segura
   - `.env` no se incluye en Git
   - Scripts de deploy actualizados

---

## 🚀 CONFIGURACIÓN PARA PRODUCCIÓN

### 1. **GENERAR SECRET_KEY ÚNICO**
```bash
# En el servidor de producción:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. **CONFIGURAR .env DE PRODUCCIÓN**
```env
# Copiar desde .env.example y personalizar:
DATABASE_URL=postgresql://usuario_seguro:password_muy_fuerte@localhost:5432/delizzia_pos
SECRET_KEY=TU_SECRET_KEY_GENERADO_AQUI
ENVIRONMENT=production
SQL_ECHO=false
CORS_ORIGINS=https://tudominio.com
```

### 3. **CREAR USUARIO ADMINISTRADOR**
```bash
cd backend
python scripts/create_admin.py
```

### 4. **CONFIGURAR BASE DE DATOS**
```sql
-- PostgreSQL para producción
CREATE DATABASE delizzia_pos;
CREATE USER delizzia_user WITH ENCRYPTED PASSWORD 'password_muy_seguro';
GRANT ALL PRIVILEGES ON DATABASE delizzia_pos TO delizzia_user;
```

---

## 🛡️ CHECKLIST DE SEGURIDAD PRE-DEPLOY

### ✅ **ANTES DE DESPLEGAR:**

- [ ] **Nuevo SECRET_KEY generado** (nunca usar el de desarrollo)
- [ ] **Contraseñas de BD únicas** (no usar "delizzia_password")
- [ ] **Usuario admin creado** con contraseña segura
- [ ] **SQL_ECHO=false** en producción
- [ ] **CORS configurado** solo para dominios válidos
- [ ] **HTTPS habilitado** en servidor web
- [ ] **Firewall configurado** (solo puertos necesarios)
- [ ] **Backups automáticos** de base de datos
- [ ] **Logs de aplicación** monitoreados
- [ ] **Archivos .env** con permisos restrictivos (600)

### ⚠️ **NUNCA EN PRODUCCIÓN:**

- ❌ Usar SECRET_KEY de desarrollo
- ❌ Usar credenciales admin/admin123
- ❌ Exponer puerto 8000 directamente
- ❌ Tener SQL_ECHO=true
- ❌ Usar SQLite (usar PostgreSQL)
- ❌ Commits con archivos .env
- ❌ CORS con "*" (permitir todos)

---

## 🔒 CONFIGURACIÓN DE SERVIDOR

### **Nginx (Recomendado)**
```nginx
server {
    listen 443 ssl;
    server_name tudominio.com;
    
    # SSL Configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **Systemd Service**
```ini
[Unit]
Description=Delizzia POS Backend
After=network.target

[Service]
Type=simple
User=delizzia
WorkingDirectory=/opt/delizzia-pos/backend
Environment=PATH=/opt/delizzia-pos/backend/venv/bin
ExecStart=/opt/delizzia-pos/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 📋 MONITOREO Y MANTENIMIENTO

### **Logs Importantes:**
```bash
# Logs de aplicación
tail -f /var/log/delizzia/app.log

# Logs de nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Logs del sistema
journalctl -u delizzia-pos -f
```

### **Backup Automático:**
```bash
#!/bin/bash
# /opt/delizzia-pos/backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump delizzia_pos > /backups/delizzia_$DATE.sql
gzip /backups/delizzia_$DATE.sql

# Eliminar backups antiguos (más de 30 días)
find /backups -name "delizzia_*.sql.gz" -mtime +30 -delete
```

---

## 🆘 RESPUESTA A INCIDENTES

### **Si SECRET_KEY está comprometido:**
1. **INMEDIATAMENTE** generar nuevo SECRET_KEY
2. Actualizar `.env` en servidor
3. Reiniciar aplicación
4. Forzar logout de todos los usuarios
5. Notificar a administradores

### **Si credenciales admin están comprometidas:**
1. Cambiar contraseña inmediatamente
2. Revisar logs de acceso
3. Crear nuevo usuario admin si es necesario
4. Deshabilitar usuario comprometido

---

## 📞 CONTACTO DE EMERGENCIA

- **Repository:** https://github.com/luisrojas8320/pizzeria-pos
- **Documentación:** Ver `backend/README.md`
- **Logs:** Revisar `/var/log/delizzia/`

---

## 🎯 COMANDOS DE DESARROLLO SEGURO

```bash
# Crear admin (primera vez)
cd backend && python scripts/create_admin.py

# Generar SECRET_KEY nuevo
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Verificar configuración
cd backend && python -c "from app.core.config import settings; print(f'Environment: {settings.ENVIRONMENT}')"

# Backup manual
pg_dump delizzia_pos > backup_$(date +%Y%m%d).sql
```

**🍕 ¡Mantén Delizzia POS seguro y funcional!**