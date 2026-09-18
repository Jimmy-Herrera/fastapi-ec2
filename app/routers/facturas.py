from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Cliente, Factura, FacturaCreate, FacturaUpdate

router = APIRouter(prefix="/facturas", tags=["Facturas"])


def _validar_cliente(cliente_id: int, session: Session):
    if not session.get(Cliente, cliente_id):
        raise HTTPException(
            status_code=404, detail=f"No existe el cliente con id {cliente_id}"
        )


@router.post("/", response_model=Factura, status_code=201)
def crear_factura(datos: FacturaCreate, session: Session = Depends(get_session)):
    _validar_cliente(datos.cliente_id, session)

    factura = Factura.model_validate(datos)
    session.add(factura)
    session.commit()
    session.refresh(factura)
    return factura


@router.get("/", response_model=list[Factura])
def listar_facturas(
    cliente_id: int | None = None,
    session: Session = Depends(get_session),
):
    consulta = select(Factura)
    if cliente_id is not None:
        consulta = consulta.where(Factura.cliente_id == cliente_id)
    return session.exec(consulta).all()


@router.get("/{factura_id}", response_model=Factura)
def obtener_factura(factura_id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@router.patch("/{factura_id}", response_model=Factura)
def actualizar_factura(
    factura_id: int,
    datos: FacturaUpdate,
    session: Session = Depends(get_session),
):
    factura = session.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    cambios = datos.model_dump(exclude_unset=True)
    if "cliente_id" in cambios:
        _validar_cliente(cambios["cliente_id"], session)

    for campo, valor in cambios.items():
        setattr(factura, campo, valor)

    session.add(factura)
    session.commit()
    session.refresh(factura)
    return factura


@router.delete("/{factura_id}")
def eliminar_factura(factura_id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    session.delete(factura)
    session.commit()
    return {"ok": True, "mensaje": "Factura eliminada"}