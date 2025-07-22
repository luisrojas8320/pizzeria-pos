# Delizzia POS - Backend API

Sistema de Punto de Venta completo para Delizzia Pizzería en Ibarra, Ecuador. Backend desarrollado con FastAPI, PostgreSQL y diseñado específicamente para optimizar las operaciones de una pizzería con entregas a domicilio.

## 🚀 Características Principales

### 📊 Gestión de Pedidos
- Registro completo de pedidos con detalles de cliente y plataforma
- Cálculo automático de costos, comisiones y ganancias netas
- Integración con plataformas de delivery (Uber Eats, Pedidos Ya, Bis)
- Tracking de tiempo de entrega y estados de pedidos

### 💰 Análisis Financiero
- Cálculos automáticos de:
  - Costos de ingredientes
  - Costos de empaque
  - Comisiones por plataforma
  - Ganancias netas
- Reportes de ventas (diarios, semanales, mensuales)
- Análisis de rentabilidad por producto

### 📋 Gestión de Compras
- Órdenes de compra con proveedores
- Programación automática de compras semanales
- Control de inventario con alertas de stock mínimo
- Análisis de costos y proveedores

### 👥 Gestión de Personal
- Horarios y programación de personal
- Seguimiento de rendimiento
- Análisis de utilización de horas laborales

### 🎯 Análisis de Clientes
- Identificación de clientes frecuentes
- Análisis de comportamiento de compra
- Segmentación de clientes
- Métricas de satisfacción

### 📈 Análisis y Predicciones
- Predicción de demanda usando algoritmos de ML
- Análisis de tendencias específicas para Ibarra
- Optimización de precios y menú
- Recomendaciones de negocio

## 🛠️ Stack Tecnológico

- **Framework**: FastAPI 0.104+
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Autenticación**: JWT con python-jose
- **Validación**: Pydantic v2
- **Cache**: Redis
- **Tareas Asíncronas**: Celery
- **Análisis**: Pandas, NumPy, Scikit-learn

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── api/                    # Endpoints de la API
│   │   ├── auth.py            # Autenticación
│   │   ├── orders.py          # Gestión de pedidos
│   │   ├── purchases.py       # Gestión de compras
│   │   ├── menu.py            # Gestión de menú
│   │   ├── staff.py           # Gestión de personal
│   │   ├── customers.py       # Gestión de clientes
│   │   ├── analytics.py       # Análisis y métricas
│   │   └── platforms.py       # Análisis de plataformas
│   ├── core/                  # Configuración central
│   │   ├── config.py         # Configuraciones
│   │   ├── database.py       # Conexión a BD
│   │   ├── security.py       # Seguridad y JWT
│   │   └── auth.py           # Middleware de autenticación
│   ├── models/               # Modelos SQLAlchemy
│   │   ├── users.py         # Usuarios del sistema
│   │   ├── orders.py        # Pedidos y items
│   │   ├── menu.py          # Menú y categorías
│   │   ├── inventory.py     # Inventario y proveedores
│   │   ├── purchases.py     # Compras y programación
│   │   ├── staff.py         # Personal y horarios
│   │   └── customers.py     # Clientes y feedback
│   ├── schemas/             # Esquemas Pydantic
│   ├── services/            # Lógica de negocio
│   │   ├── orders.py       # Servicio de pedidos
│   │   └── calculations.py # Cálculos financieros
│   ├── utils/              # Utilidades
│   │   ├── predictions.py  # Algoritmos de predicción
│   │   └── optimization.py # Optimización de negocio
│   └── main.py            # Punto de entrada
├── requirements.txt        # Dependencias
├── .env.example           # Variables de entorno
├── README.md             # Documentación
└── alembic/             # Migraciones de BD
```

## ⚙️ Instalación y Configuración

### Prerrequisitos
- Python 3.9+
- PostgreSQL 13+
- Redis (opcional, para cache)

### 1. Clonar el Repositorio
```bash
cd delizzia-pos/backend
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate     # En Windows
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 5. Configurar Base de Datos
```bash
# Crear base de datos PostgreSQL
createdb delizzia_pos

# Ejecutar migraciones
alembic upgrade head
```

### 6. Crear Usuario Administrador
```python
# Ejecutar script de inicialización (crear según necesidad)
python scripts/create_admin.py
```

## 🚀 Ejecución

### Desarrollo
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📊 API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario (solo owners)
- `GET /api/auth/me` - Información del usuario actual

### Pedidos
- `POST /api/orders/` - Crear pedido
- `GET /api/orders/` - Listar pedidos
- `GET /api/orders/{id}` - Obtener pedido
- `PUT /api/orders/{id}` - Actualizar pedido
- `GET /api/orders/reports/daily` - Reporte diario
- `GET /api/orders/reports/weekly` - Reporte semanal
- `GET /api/orders/reports/monthly` - Reporte mensual

### Compras
- `POST /api/purchases/` - Crear orden de compra
- `GET /api/purchases/` - Listar órdenes
- `GET /api/purchases/schedules/weekly` - Programación semanal
- `POST /api/purchases/suppliers/` - Crear proveedor

### Menú
- `POST /api/menu/categories/` - Crear categoría
- `GET /api/menu/categories/` - Listar categorías
- `POST /api/menu/items/` - Crear item de menú
- `GET /api/menu/items/` - Listar items
- `PUT /api/menu/items/{id}` - Actualizar item

### Personal
- `GET /api/staff/` - Listar personal
- `GET /api/staff/schedules/weekly` - Horario semanal
- `GET /api/staff/performance/summary` - Resumen de rendimiento

### Clientes
- `GET /api/customers/frequent/` - Clientes frecuentes
- `GET /api/customers/analytics/segmentation` - Segmentación
- `GET /api/customers/analytics/retention` - Retención

### Análisis
- `GET /api/analytics/trends/demand` - Tendencias de demanda
- `GET /api/analytics/optimization/pricing` - Optimización de precios
- `GET /api/analytics/predictions/sales` - Predicciones de ventas
- `GET /api/analytics/kpis/dashboard` - KPIs del dashboard

### Plataformas
- `GET /api/platforms/performance/` - Rendimiento por plataforma
- `GET /api/platforms/commission/analysis` - Análisis de comisiones
- `GET /api/platforms/visibility/recommendations` - Recomendaciones

## 🔧 Configuración Específica

### Tasas de Comisión por Plataforma
```python
COMMISSION_RATES = {
    "uber_eats": 0.30,     # 30%
    "pedidos_ya": 0.28,    # 28%
    "bis": 0.25,           # 25%
    "phone": 0.0,          # 0%
    "whatsapp": 0.0,       # 0%
}
```

### Costos de Empaque
```python
PACKAGING_COSTS = {
    "small_box": 0.15,     # $0.15
    "medium_box": 0.20,    # $0.20
    "large_box": 0.25,     # $0.25
    "drinks": 0.05,        # $0.05
    "utensils": 0.03,      # $0.03
}
```

## 📈 Funcionalidades Específicas para Ibarra

### Análisis de Tendencias Locales
- Patrones de consumo durante festivales (Inti Raymi, Fiesta de los Lagos)
- Correlación con calendario universitario (UTN)
- Análisis de días de pago (15 y 30 de cada mes)
- Impacto del clima en pedidos de delivery

### Optimización para Pizzería
- Cálculo de costos de ingredientes por pizza
- Análisis de tiempo de preparación vs demanda
- Optimización de rutas de delivery en Ibarra
- Gestión de inventario específica para ingredientes perecederos

## 🔒 Seguridad

- Autenticación JWT con expiración configurable
- Roles de usuario (owner, staff)
- Validación de datos con Pydantic
- Sanitización de inputs
- Rate limiting (implementar según necesidad)

## 📊 Métricas y KPIs

### Financieros
- Ingresos totales y netos
- Margen de ganancia por pedido
- Costo de ingredientes vs ingresos
- Impacto de comisiones por plataforma

### Operacionales
- Tiempo promedio de preparación
- Tiempo promedio de entrega
- Eficiencia del personal
- Rotación de inventario

### Clientes
- Valor promedio de pedido
- Frecuencia de pedidos
- Retención de clientes
- Net Promoter Score (NPS)

## 🚀 Deployment

### Docker (Recomendado)
```bash
# Crear imagen
docker build -t delizzia-pos-api .

# Ejecutar contenedor
docker run -d --name delizzia-api -p 8000:8000 delizzia-pos-api
```

### Usando Gunicorn
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=app tests/
```

## 📝 API Documentation

Una vez iniciado el servidor, la documentación interactiva está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contribuciones

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para soporte técnico o consultas:
- Email: soporte@delizzia.com
- Issues: GitHub Issues

## 🗺️ Roadmap

### Próximas Funcionalidades
- [ ] Integración con APIs de delivery platforms
- [ ] Sistema de notificaciones en tiempo real
- [ ] App móvil para personal
- [ ] Análisis predictivo avanzado con ML
- [ ] Sistema de loyalty points
- [ ] Integración con sistemas de pago
- [ ] Dashboard en tiempo real
- [ ] Reportes automatizados por email

---

**Desarrollado con ❤️ para Delizzia Pizzería, Ibarra - Ecuador**