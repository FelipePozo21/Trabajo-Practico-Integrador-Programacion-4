# Food Store · Trabajo Práctico Integrador

Aplicación de pedidos de comida implementada con FastAPI, SQLModel y PostgreSQL (SQLite para desarrollo), más React, TypeScript y Vite.

# Repositorio

https://github.com/FelipePozo21/Trabajo-Practico-Integrador-Programacion-4

# Video

https://youtu.be/EvBBpiy26P8

## Requisitos

- Python 3.11–3.14 (SQLModel fijado en 0.0.50)
- Node.js 20.19 o superior y pnpm 9+
- PostgreSQL 15+ (opcional para desarrollo local; SQLite funciona por defecto)

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      
pip install -r requirements.txt
cp .env.example .env         
python -m app.db.seed
uvicorn app.main:app --reload
```

Si ya tenías un entorno creado con SQLModel 0.0.22, recrealo antes de instalar: `deactivate` y luego elimina `.venv` desde la carpeta `backend` para crear el entorno nuevo. El proyecto fija SQLModel 0.0.50 para que también arranque en Python 3.14.

API: <http://localhost:8000/api/v1>, documentación: <http://localhost:8000/docs> y <http://localhost:8000/redoc>.

Variables disponibles en `backend/.env.example`: `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` y `FRONTEND_ORIGIN`. Para PostgreSQL, configurar `DATABASE_URL=postgresql://usuario:clave@localhost:5432/foodstore_db`.

El seed crea o restablece el administrador demo `admin` con contraseña `Admin1234!`, tres categorías y nueve productos. Es idempotente; al volver a ejecutarlo restablece la contraseña del administrador demo.

## Frontend

```bash
cd frontend
cp .env.example .env
pnpm install
pnpm dev
```

La aplicación queda en <http://localhost:5173>. `VITE_API_URL` debe apuntar al backend, por defecto `http://localhost:8000/api/v1`. Para compilar y verificar TypeScript: `pnpm build`.

## Funcionalidad

Registro y login con cookie HttpOnly; catálogo paginado y filtrable; carrito persistido; checkout y consulta/cancelación de pedidos; administración de categorías, productos, stock, pedidos, usuarios e indicadores. El backend aplica los roles, transiciones y cambios de stock en la capa de negocio.

Repositorio: completar con la URL pública al publicar el proyecto.

Video de demostración: completar el enlace al grabar la entrega.
