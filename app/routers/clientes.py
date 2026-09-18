from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Cliente, ClienteCreate, ClienteUpdate, Factura

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=Cliente, status_code=201)
def crear_cliente(datos: ClienteCreate, session: Session = Depends(get_session)):
    existente = session.exec(
        select(Cliente).where(Cliente.cedula == datos.cedula)
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un cliente con esa cédula")

    cliente = Cliente.model_validate(datos)
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@router.get("/", response_model=list[Cliente])
def listar_clientes(session: Session = Depends(get_session)):
    return session.exec(select(Cliente)).all()


@router.get("/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.patch("/{cliente_id}", response_model=Cliente)
def actualizar_cliente(
    cliente_id: int,
    datos: ClienteUpdate,
    session: Session = Depends(get_session),
):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(cliente, campo, valor)

    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    facturas = session.exec(
        select(Factura).where(Factura.cliente_id == cliente_id)
    ).all()
    if facturas:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar: el cliente tiene facturas registradas",
        )

    session.delete(cliente)
    session.commit()
    return {"ok": True, "mensaje": "Cliente eliminado"}