# 🍕 DELIZZIA POS - INSTRUCCIONES PARA USUARIO

## 🚀 INICIO RÁPIDO (1 MINUTO)

### ✅ OPCIÓN 1: ACCESO DIRECTO EN ESCRITORIO
1. **Hacer doble clic** en `CREAR_ACCESO_DIRECTO.bat`
2. **Hacer doble clic** en el ícono "Delizzia POS" que aparece en el escritorio
3. **¡LISTO!** El sistema se abre automáticamente en el navegador

### ✅ OPCIÓN 2: ARCHIVO DIRECTO
1. **Hacer doble clic** en `INICIAR_DELIZZIA_POS.bat`
2. **Esperar 15 segundos** mientras se inicia todo
3. **¡LISTO!** Se abre automáticamente en http://localhost:3000

---

## 🛑 PARA DETENER EL SISTEMA
- **Hacer doble clic** en `DETENER_DELIZZIA_POS.bat`
- O cerrar las ventanas de terminal que se abrieron

---

## 🔧 REQUISITOS (SE INSTALAN AUTOMÁTICAMENTE)
- ✅ Python 3.9+ (se verifica automáticamente)
- ✅ Node.js (se verifica automáticamente)
- ✅ Base de datos SQLite (se crea automáticamente)
- ✅ Todas las dependencias (se instalan automáticamente)

---

## 🌐 ACCEDER AL SISTEMA

### 📊 **Dashboard Principal**
- **URL:** http://localhost:3000
- **👤 Usuario:** Crear usando script de administrador
- **🔐 Contraseña:** La que generes durante inicialización

⚠️ **IMPORTANTE**: Debes crear el usuario administrador usando:
```cmd
cd backend
python scripts/create_admin.py
```

### 📡 **Documentación API**
- **URL:** http://localhost:8000/docs
- **Para desarrolladores/técnicos**

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### ❌ "Python no encontrado"
1. Descargar Python desde: https://python.org
2. Durante instalación marcar "Add to PATH"
3. Reiniciar computadora

### ❌ "Node.js no encontrado"
1. Descargar Node.js desde: https://nodejs.org
2. Instalar versión LTS (recomendada)
3. Reiniciar computadora

### ❌ "Puerto ocupado"
1. Ejecutar `DETENER_DELIZZIA_POS.bat`
2. Esperar 30 segundos
3. Ejecutar `INICIAR_DELIZZIA_POS.bat` nuevamente

### ❌ "Error de permisos"
1. Hacer clic derecho en `INICIAR_DELIZZIA_POS.bat`
2. Seleccionar "Ejecutar como administrador"

---

## 📱 FUNCIONALIDADES PRINCIPALES

### 📊 **Dashboard**
- Ver ventas del día en tiempo real
- Gráficos de rendimiento
- Alertas de inventario
- Estado del personal

### 📋 **Gestión de Pedidos**
- Crear nuevos pedidos
- Seguimiento de entregas
- Cálculo automático de ganancias
- Análisis por plataforma (Uber Eats, Pedidos Ya, etc.)

### 💰 **Análisis Financiero**
- Reportes de ganancias automáticos
- Análisis de costos por producto
- Comparación entre plataformas
- Predicciones de demanda

### 👥 **Gestión de Clientes**
- Clientes frecuentes
- Historial de pedidos
- Análisis de comportamiento
- Segmentación automática

---

## 🔄 ACTUALIZACIONES

Para obtener nuevas funcionalidades:
1. Descargar nueva versión desde GitHub
2. Reemplazar archivos
3. Ejecutar `INICIAR_DELIZZIA_POS.bat` normalmente

---

## 📞 SOPORTE

- **GitHub:** https://github.com/luisrojas8320/pizzeria-pos
- **Email:** luisrojas8320@gmail.com
- **Documentación:** Ver carpeta `backend/README.md`

---

## 🎯 TIPS DE USO

1. **Primer uso:** El sistema tarda 1-2 minutos en configurarse
2. **Uso diario:** Solo 15 segundos en iniciar
3. **Datos:** Se guardan automáticamente en `backend/delizzia_pos.db`
4. **Backup:** Copiar el archivo `delizzia_pos.db` para respaldar datos
5. **Navegador:** Funciona mejor en Chrome, Firefox o Edge

**🍕 ¡Disfruta usando Delizzia POS!**