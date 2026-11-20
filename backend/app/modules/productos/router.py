from fastapi import APIRouter, Depends, Response, Query, HTTPException
from app.core.deps import require_role
from app.core.domain_errors import DomainError
from app.modules.usuarios.models import Usuario
from app.modules.productos.schemas import ProductoCreate,ProductoUpdate,ProductoStockUpdate,ProductoRead,ProductosPaginados
from app.modules.productos.service import ProductoService
router=APIRouter(prefix="/productos",tags=["productos"])

def get_producto_service() -> ProductoService:
    return ProductoService()

def _translate(call):
    try:
        return call()
    except DomainError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error

@router.get("/admin",response_model=ProductosPaginados)
def list_products_admin(
    skip:int=Query(0,ge=0),limit:int=Query(20,ge=1,le=100),search:str|None=None,
    categoria_id:int|None=None,disponible:bool|None=None,
    _:Usuario=Depends(require_role(["admin"])),service:ProductoService=Depends(get_producto_service),
):
    return _translate(lambda: service.list_active(skip,limit,search,categoria_id,disponible))

@router.get("",response_model=ProductosPaginados)
def list_products(
    skip:int=Query(0,ge=0),limit:int=Query(20,ge=1,le=100),search:str|None=None,
    categoria_id:int|None=None,disponible:bool|None=None,
    service:ProductoService=Depends(get_producto_service),
):
    solo_vendibles=True
    return _translate(lambda: service.list_active(skip,limit,search,categoria_id,disponible,solo_vendibles))
@router.get("/{pid}",response_model=ProductoRead)
def get_product(pid:int,service:ProductoService=Depends(get_producto_service)): return _translate(lambda: service.get(pid,solo_vendibles=True))
@router.post("",response_model=ProductoRead,status_code=201)
def create(data:ProductoCreate,_:Usuario=Depends(require_role(["admin"])),service:ProductoService=Depends(get_producto_service)): return _translate(lambda: service.create(data))
@router.put("/{pid}",response_model=ProductoRead)
def update(pid:int,data:ProductoUpdate,_:Usuario=Depends(require_role(["admin"])),service:ProductoService=Depends(get_producto_service)): return _translate(lambda: service.update(pid,data))
@router.patch("/{pid}/stock",response_model=ProductoRead)
def stock(pid:int,data:ProductoStockUpdate,_:Usuario=Depends(require_role(["admin"])),service:ProductoService=Depends(get_producto_service)): return _translate(lambda: service.update_stock(pid,data))
@router.delete("/{pid}",status_code=204)
def delete(pid:int,_:Usuario=Depends(require_role(["admin"])),service:ProductoService=Depends(get_producto_service)):
    _translate(lambda: service.deactivate(pid));return Response(status_code=204)
