from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.deps import get_current_active_user, require_role
from app.modules.usuarios.models import Usuario
from app.modules.pedidos.schemas import CambioEstado, PedidoCreate, PedidoRead, PedidosPaginados, ResumenPedidos
from app.modules.pedidos.service import PedidoError, PedidoService

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

def get_pedido_service() -> PedidoService:
    return PedidoService()

def _translate_error(error: PedidoError) -> HTTPException:
    return HTTPException(status_code=error.status_code, detail=error.detail)

@router.post("", response_model=PedidoRead, status_code=201)
def create(data: PedidoCreate, user: Usuario = Depends(get_current_active_user), service: PedidoService = Depends(get_pedido_service)):
    try:
        return service.create(user.id, data)
    except PedidoError as error:
        raise _translate_error(error) from error

@router.get("", response_model=PedidosPaginados)
def list_orders(
    skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), estado: str | None = None,
    user: Usuario = Depends(get_current_active_user), service: PedidoService = Depends(get_pedido_service),
):
    return service.list_orders(user.id, user.role == "admin", skip, limit, estado)

@router.get("/mios", response_model=PedidosPaginados)
def list_my_orders(
    skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), estado: str | None = None,
    user: Usuario = Depends(get_current_active_user), service: PedidoService = Depends(get_pedido_service),
):
    return service.list_orders(user.id, user.role == "admin", skip, limit, estado, own_only=True)

@router.get("/resumen", response_model=ResumenPedidos)
def summary(_: Usuario = Depends(require_role(["admin"])), service: PedidoService = Depends(get_pedido_service)):
    return service.summary()

@router.get("/{pid}", response_model=PedidoRead)
def get_order(pid: int, user: Usuario = Depends(get_current_active_user), service: PedidoService = Depends(get_pedido_service)):
    try:
        return service.get(pid, user.id, user.role == "admin")
    except PedidoError as error:
        raise _translate_error(error) from error

@router.patch("/{pid}/estado", response_model=PedidoRead)
def change_state(
    pid: int, data: CambioEstado, _: Usuario = Depends(require_role(["admin"])),
    service: PedidoService = Depends(get_pedido_service),
):
    try:
        return service.transition(pid, data.estado)
    except PedidoError as error:
        raise _translate_error(error) from error

@router.patch("/{pid}/cancelar", response_model=PedidoRead)
def cancel(pid: int, user: Usuario = Depends(get_current_active_user), service: PedidoService = Depends(get_pedido_service)):
    try:
        if user.role == "admin":
            return service.transition(pid, "CANCELADO")
        return service.cancel_for_user(pid, user.id)
    except PedidoError as error:
        raise _translate_error(error) from error
