from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import crear_tablas
from app.routers import clientes, facturas


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield


app = FastAPI(
    title="API de Facturación",
    description="API RESTful con operaciones CRUD para Clientes y Facturas",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(clientes.router)
app.include_router(facturas.router)


@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API de Facturación activa", "documentacion": "/docs"}