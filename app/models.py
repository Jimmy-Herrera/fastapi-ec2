from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field


class ClienteBase(SQLModel):
    nombre: str
    cedula: str = Field(index=True, unique=True)
    email: str
    telefono: Optional[str] = None


class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(SQLModel):
    nombre: Optional[str] = None
    cedula: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


class FacturaBase(SQLModel):
    numero: str
    descripcion: str
    monto: float
    fecha: date = Field(default_factory=date.today)
    cliente_id: int = Field(foreign_key="cliente.id")


class Factura(FacturaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class FacturaCreate(FacturaBase):
    pass


class FacturaUpdate(SQLModel):
    numero: Optional[str] = None
    descripcion: Optional[str] = None
    monto: Optional[float] = None
    fecha: Optional[date] = None
    cliente_id: Optional[int] = None