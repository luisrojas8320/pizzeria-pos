# 🍕 Delizzia POS - Sistema Integral de Punto de Venta

Sistema de Punto de Venta completo para **Delizzia Pizzería** en Ibarra, Ecuador. Diseñado específicamente para optimizar operaciones de pizzería con delivery, análisis financiero avanzado y predicciones de demanda.

## 📋 Descripción del Proyecto

**Delizzia POS** es una solución integral que combina:
- **Frontend**: Next.js 15 con React 19, TypeScript y Tailwind CSS
- **Backend**: FastAPI con PostgreSQL, algoritmos de ML y análisis predictivo
- **Funcionalidades**: Gestión completa de pedidos, inventario, personal, clientes y análisis financiero

### 🎯 Características Principales

#### 📊 Gestión de Pedidos
- Registro completo de pedidos con integración a plataformas (Uber Eats, Pedidos Ya, Bis)
- Cálculo automático de costos, comisiones y ganancias netas
- Tracking en tiempo real de estados de pedidos
- Reportes automáticos (diarios, semanales, mensuales)

#### 💰 Análisis Financiero Inteligente
- **Cálculos Automáticos:**
  - Costos de ingredientes por producto
  - Costos de empaque optimizados
  - Comisiones por plataforma de delivery
  - Ganancias netas en tiempo real
- **KPIs del Negocio:**
  - Margen de ganancia por pedido
  - Rendimiento por plataforma
  - Análisis de rentabilidad por producto

#### 🏪 Gestión Integral
- **Inventario**: Control de stock con alertas automáticas
- **Compras**: Órdenes programadas con proveedores
- **Personal**: Horarios, rendimiento y optimización
- **Clientes**: Segmentación, retención y análisis de comportamiento

#### 🤖 Inteligencia de Negocio
- **Predicciones de Demanda** usando Machine Learning
- **Optimización de Precios** basada en costos y demanda
- **Análisis Específico para Ibarra**: 
  - Patrones universitarios (UTN)
  - Festivales locales (Inti Raymi, Fiesta de los Lagos)
  - Ciclos de pago (15 y 30 de cada mes)

## 🏗️ Arquitectura del Sistema

### Frontend (Next.js)
```
app/
├── analytics/          # Dashboards y métricas
├── customers/          # Gestión de clientes
├── inventory/          # Control de inventario
├── menu/              # Gestión de menú
├── orders/            # Gestión de pedidos
├── purchases/         # Órdenes de compra
├── reports/           # Reportes financieros
├── staff/             # Gestión de personal
└── components/        # Componentes reutilizables
```

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/           # Endpoints RESTful
│   ├── core/          # Configuración y seguridad
│   ├── models/        # Modelos de base de datos
│   ├── schemas/       # Validación de datos
│   ├── services/      # Lógica de negocio
│   └── utils/         # Algoritmos de ML y optimización
```

## 🚀 Tecnologías Utilizadas

### Frontend
- **Next.js 15** - Framework React con App Router
- **React 19** - Biblioteca UI con Server Components
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Styling utility-first
- **shadcn/ui** - Componentes accesibles y modernos
- **Recharts** - Visualización de datos

### Backend
- **FastAPI** - Framework Python moderno y rápido
- **PostgreSQL** - Base de datos relacional
- **SQLAlchemy** - ORM avanzado
- **JWT Authentication** - Seguridad y autorización
- **Pydantic** - Validación de datos
- **Pandas & NumPy** - Análisis de datos
- **Scikit-learn** - Machine Learning

### Infraestructura
- **Redis** - Cache y sesiones
- **Celery** - Tareas asíncronas
- **Alembic** - Migraciones de BD
- **Docker** - Containerización

## ⚙️ Instalación y Configuración

### Prerrequisitos
- Node.js 18+ y pnpm
- Python 3.9+ 
- PostgreSQL 13+
- Redis (opcional)

### 1. Clonar Repositorio
```bash
git clone https://github.com/luisrojas8320/pizzeria-pos.git
cd pizzeria-pos
```

### 2. Configurar Frontend
```bash
# Instalar dependencias
pnpm install

# Configurar variables de entorno
cp .env.example .env.local

# Iniciar desarrollo
pnpm dev
```

### 3. Configurar Backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Configurar base de datos
createdb delizzia_pos
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

## 📊 API Endpoints Principales

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario
- `GET /api/auth/me` - Perfil actual

### Pedidos
- `POST /api/orders` - Crear pedido
- `GET /api/orders/reports/daily` - Reporte diario
- `GET /api/orders/analytics/popular-items` - Items populares

### Análisis
- `GET /api/analytics/trends/demand` - Tendencias de demanda
- `GET /api/analytics/predictions/sales` - Predicciones de ventas
- `GET /api/analytics/kpis/dashboard` - KPIs principales

### Plataformas
- `GET /api/platforms/performance` - Rendimiento por plataforma
- `GET /api/platforms/commission/analysis` - Análisis de comisiones

## 💼 Funcionalidades de Negocio

### Análisis Específico para Ibarra 🇪🇨

#### Contexto Local
- **Patrones Universitarios**: Análisis de demanda basado en calendario académico UTN
- **Festivales Locales**: Optimización para Inti Raymi, Fiesta de los Lagos
- **Ciclos Económicos**: Patrones de consumo en días de pago (15 y 30)
- **Clima**: Correlación entre clima y pedidos de delivery

#### Optimización de Plataformas
- **Uber Eats**: 30% comisión - Análisis de rentabilidad
- **Pedidos Ya**: 28% comisión - Estrategias de visibilidad
- **Bis**: 25% comisión - Crecimiento en Ecuador
- **Directo (WhatsApp/Teléfono)**: 0% comisión - Promoción activa

### Algoritmos de Machine Learning

#### Predicción de Demanda
```python
# Modelos implementados:
- Análisis de tendencias temporales
- Predicciones estacionales
- Ensemble con múltiples algoritmos
- Intervalos de confianza
```

#### Optimización de Negocio
```python
# Algoritmos incluidos:
- Optimización de precios por elasticidad de demanda
- Economic Order Quantity (EOQ) para inventario
- Optimización de horarios de personal
- Análisis de mix de menú (Stars, Plowhorses, Puzzles, Dogs)
```

## 📈 Dashboard y Métricas

### KPIs Principales
- **Financieros**: Ingresos, costos, margen de ganancia
- **Operacionales**: Tiempo de preparación, eficiencia de entrega
- **Clientes**: Valor promedio de pedido, retención, NPS
- **Personal**: Productividad, utilización de horas

### Reportes Automáticos
- Reportes diarios enviados por email
- Análisis semanal de tendencias
- Reportes mensuales con predicciones
- Alertas de stock bajo e ineficiencias

## 🔒 Seguridad

- **Autenticación JWT** con roles (owner/staff)
- **Validación de datos** en frontend y backend
- **Encriptación de contraseñas** con bcrypt
- **HTTPS obligatorio** en producción
- **Rate limiting** para APIs
- **Sanitización de inputs** contra inyecciones

## 🚀 Deployment

### Desarrollo Local
```bash
# Frontend
pnpm dev

# Backend
uvicorn app.main:app --reload
```

### Producción con Docker
```bash
# Build y deploy completo
docker-compose up --build -d
```

### Variables de Entorno Críticas
```env
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/delizzia_pos
SECRET_KEY=your-super-secret-key-change-in-production
REDIS_URL=redis://localhost:6379/0

# Frontend
NEXT_PUBLIC_API_URL=https://api.delizzia.com
NEXT_PUBLIC_APP_URL=https://pos.delizzia.com
```

## 📊 Casos de Uso Específicos

### 1. Registro de Pedido Completo
```typescript
// Flujo automático:
1. Cliente hace pedido por Uber Eats
2. Sistema calcula automáticamente:
   - Costo de ingredientes: $3.50
   - Costo de empaque: $0.20
   - Comisión Uber Eats (30%): $6.00
   - Ganancia neta: $10.30
3. Actualiza inventario automáticamente
4. Genera métricas en tiempo real
```

### 2. Análisis de Rentabilidad
```python
# Análisis automático por producto:
- Pizza Margherita: 65% margen - ⭐ STAR
- Pizza Hawaiana: 45% margen, alta demanda - 🐴 PLOWHORSE
- Pizza Vegana: 70% margen, baja demanda - 🧩 PUZZLE
- Pizza Anchoas: 25% margen, baja demanda - 🐕 DOG (considerar remover)
```

### 3. Predicción de Demanda Inteligente
```python
# Predicciones contextuales:
- Viernes 15 de mes + lluvia = +40% pedidos
- Semana de exámenes UTN = -20% pedidos
- Inti Raymi = +100% pedidos durante festival
- Domingo = -30% pedidos (patrón semanal)
```

## 📞 Soporte y Contribuciones

### Contacto
- **Desarrollador**: Luis Rojas
- **Email**: luisrojas8320@gmail.com
- **GitHub**: [luisrojas8320](https://github.com/luisrojas8320)

### Contribuir
1. Fork del proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para detalles.

---

### 🎯 Roadmap Futuro

#### Q1 2025
- [ ] App móvil para repartidores
- [ ] Integración directa APIs de delivery
- [ ] Sistema de loyalty points
- [ ] Notificaciones push en tiempo real

#### Q2 2025
- [ ] IA avanzada para predicción de demanda
- [ ] Integración con sistemas de pago
- [ ] Análisis de sentimientos de reviews
- [ ] Optimización automática de rutas

#### Q3 2025
- [ ] Multi-tenant para otras pizzerías
- [ ] Dashboard ejecutivo avanzado
- [ ] Integración con redes sociales
- [ ] Sistema de marketing automatizado

---

**🍕 Desarrollado con ❤️ para Delizzia Pizzería - Ibarra, Ecuador**

*Sistema completo de POS diseñado para maximizar ganancias y optimizar operaciones en el contexto específico del mercado de Ibarra.*