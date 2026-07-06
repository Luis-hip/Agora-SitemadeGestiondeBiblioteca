# Ágora — Sistema de Gestión de Biblioteca

Sistema web full-stack para la gestión integral de una biblioteca universitaria: catálogo de libros, préstamos, multas por atraso, perfil de usuario y panel administrativo para bibliotecarios.

Proyecto desarrollado como parte del curso de **Desarrollo Basado en Modelos** (Benemérita Universidad Autónoma de Puebla), siguiendo un proceso de Model-Driven Development a partir de un CIM (Modelo Independiente de Cómputo) y un PIM/PSM (Modelo Independiente/Específico de Plataforma).

## Stack tecnológico

**Backend**
- Django 6 + Django REST Framework
- PostgreSQL
- djangorestframework-simplejwt (autenticación JWT con doble actor: `Usuario` y `Bibliotecario`)
- python-decouple (configuración por variables de entorno)
- Faker (generación de datos de prueba)

**Frontend**
- Angular 22 (standalone components, Signals para manejo de estado — sin RxJS en plantillas/estado de componentes)
- Tailwind CSS 4
- Arquitectura por *features* (catálogo, perfil, admin, auth, landing)

**Arquitectura backend**

El backend sigue una arquitectura en capas:

```
Controladores (views.py / views_admin.py)
        ↓
Servicios (services/*.py)   → lógica de negocio, transacciones atómicas
        ↓
Repositorios (repositories/*.py) → acceso a datos vía ORM
```

## Funcionalidades principales

- **Autenticación JWT** con roles diferenciados: `ESTUDIANTE`, `PROFESOR` (tipo `Usuario`) y `BIBLIOTECARIO`/`ADMIN` (tipo `Bibliotecario`).
- **Catálogo público**: búsqueda y filtrado por categoría/disponibilidad, portadas reales obtenidas dinámicamente desde la API de [OpenLibrary](https://openlibrary.org/dev/docs/api/covers) a partir del ISBN.
- **Préstamos**: solicitud de préstamo con validación de reglas de negocio (límite de préstamos simultáneos, multas pendientes, disponibilidad de ejemplares, control de `stock`).
- **Motor de multas**: cálculo automático de multas por atraso, suspensión automática de usuarios morosos, pago simulado y anulación de multas por parte de un bibliotecario (con justificación).
- **Perfil de usuario**: préstamos activos, historial, multas pendientes/pagadas.
- **Panel administrativo** (bibliotecario): dashboard con KPIs, CRUD de catálogo (libros/categorías/autores), gestión de usuarios (suspender/reactivar), configuración editable de la biblioteca (tarifa de multa diaria, días máximos de préstamo).
- **Notificaciones globales** y sistema de toasts para feedback de acciones.
- **Avatares dinámicos** vía [ui-avatars.com](https://ui-avatars.com/) para vistas autenticadas.

## Estructura del repositorio

```
agora-biblioteca/
├── backend/
│   ├── core/                  # Configuración del proyecto Django (settings, urls raíz)
│   └── biblioteca/
│       ├── models.py           # Entidades del dominio (Usuario, Bibliotecario, Libro, Prestamo, Multa, etc.)
│       ├── serializers.py
│       ├── views.py            # Endpoints públicos y de usuario
│       ├── views_admin.py      # Endpoints del panel administrativo
│       ├── permissions.py      # EsUsuario / EsBibliotecario
│       ├── authentication.py   # ActorJWTAuthentication (resuelve Usuario o Bibliotecario)
│       ├── services/           # Lógica de negocio (prestamo_service, multa_service, dashboard_service, ...)
│       ├── repositories/       # Acceso a datos vía ORM
│       └── management/commands/seed_db.py  # Seeder de datos de prueba
└── frontend/
    └── src/app/
        ├── core/                # Servicios base, interceptores, modelos compartidos
        ├── shared/              # Componentes reutilizables (navbar, toasts, modales, book-cover, etc.)
        └── features/
            ├── landing/         # Landing page pública
            ├── auth/            # Login / Registro
            ├── catalogo/        # Catálogo público de libros
            ├── perfil/          # Perfil del usuario autenticado
            └── admin/           # Panel del bibliotecario (dashboard, catálogo, usuarios, ajustes)
```

## Requisitos previos

- Python 3.12+
- Node.js 20+ y npm
- PostgreSQL 14+ (o SQLite para pruebas rápidas, ver más abajo)

## Puesta en marcha

### 1. Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Crea un archivo `.env` en `backend/` (puedes copiar `.env.example`) con al menos:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=agora_biblioteca
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

TARIFA_MULTA_DIA=5.00
CORS_ALLOWED_ORIGINS=http://localhost:4200
```

> Para evitar instalar PostgreSQL localmente, puedes usar SQLite agregando `DB_ENGINE=django.db.backends.sqlite3` y `DB_NAME=db.sqlite3` a tu `.env`.

Aplica las migraciones y (opcionalmente) genera datos de prueba:

```bash
python manage.py migrate
python manage.py seed_db      # crea catálogo, usuarios y actividad de prueba
python manage.py runserver 8000
```

El comando `seed_db` es **idempotente** (puede ejecutarse varias veces sin duplicar datos) y al finalizar imprime en consola una tabla con las credenciales de todos los usuarios generados.

### 2. Frontend (Angular)

```bash
cd frontend
npm install
npm start        # equivalente a `ng serve`, sirve en http://localhost:4200
```

La app consume la API en `http://localhost:8000/api` (configurable en `frontend/src/app/core/api-base-url.ts`).

## Credenciales de prueba

Después de correr `python manage.py seed_db`, se generan (entre otros) los siguientes usuarios con contraseña `Agora2026!`:

| Usuario / Correo | Rol |
|---|---|
| `estudiante@agora.edu` | Estudiante |
| `bibliotecario` | Bibliotecario |

El resto de las credenciales generadas (estudiantes y bibliotecario adicional con datos vía Faker) se muestran en la salida del comando `seed_db`.

## Reglas de negocio destacadas

- **RN-01**: un usuario no puede tener más de 3 préstamos activos simultáneos.
- **RN-02**: la fecha de devolución esperada siempre es posterior a la fecha de inicio del préstamo (validado también a nivel de base de datos con `CheckConstraint`).
- **RN-03**: un usuario con multas pendientes queda bloqueado para nuevos préstamos y se reactiva automáticamente al liquidarlas (o si un bibliotecario anula la multa).
- **RN-04**: un ejemplar solo puede tener un préstamo activo a la vez; el `stock` disponible se descuenta al prestar y se repone al devolver.
- **RN-05**: el monto de la multa no es editable manualmente — se deriva de `tarifa_multa_diaria × días de atraso`, ambos configurables desde el panel de Ajustes.

## Scripts útiles

| Comando | Descripción |
|---|---|
| `python manage.py seed_db` | Puebla la base de datos con catálogo, usuarios y actividad de prueba |
| `python manage.py migrate` | Aplica las migraciones pendientes |
| `npm start` (frontend) | Levanta el servidor de desarrollo de Angular |
| `npm run build` (frontend) | Build de producción |

## Licencia

Proyecto académico sin licencia de distribución específica.
