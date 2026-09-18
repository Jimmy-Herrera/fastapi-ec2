# fastapi-ec2

# API de Facturación

API RESTful hecha con FastAPI, con operaciones CRUD para Clientes y Facturas, desplegada en AWS EC2.

## Tecnologías

- FastAPI
- SQLModel (ORM)
- SQLite
- Uvicorn
- pm2 (manejador de procesos en el servidor)

## Entidades

- **Clientes**: id, nombre, cédula, email, teléfono
- **Facturas**: id, número, descripción, monto, fecha, cliente_id (relación con Clientes)

## Instalación local

```bash
git clone https://github.com/jimmyjHv/api-fastapi-ec2.git
cd api-fastapi-ec2
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints

Documentación interactiva disponible en `/docs`.

- `POST /clientes/` — Crear cliente
- `GET /clientes/` — Listar clientes
- `GET /clientes/{id}` — Obtener cliente
- `PATCH /clientes/{id}` — Actualizar cliente
- `DELETE /clientes/{id}` — Eliminar cliente
- `POST /facturas/` — Crear factura
- `GET /facturas/` — Listar facturas (filtro opcional por `cliente_id`)
- `GET /facturas/{id}` — Obtener factura
- `PATCH /facturas/{id}` — Actualizar factura
- `DELETE /facturas/{id}` — Eliminar factura

## API desplegada

http://3.19.76.89:8000/docs