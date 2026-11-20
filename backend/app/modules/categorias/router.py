from fastapi import APIRouter, Depends, Response, HTTPException
from app.core.deps import require_role
from app.core.domain_errors import DomainError
from app.modules.usuarios.models import Usuario
from app.modules.categorias.schemas import CategoriaCreate,CategoriaUpdate,CategoriaRead
from app.modules.categorias.service import CategoriaService
router=APIRouter(prefix="/categorias",tags=["categorías"])

def get_categoria_service() -> CategoriaService:
    return CategoriaService()

def _translate(call):
    try:
        return call()
    except DomainError as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail) from error

@router.get("",response_model=list[CategoriaRead])
def list_cats(service:CategoriaService=Depends(get_categoria_service)): return _translate(service.list_active)
@router.get("/{cid}",response_model=CategoriaRead)
def get_cat(cid:int,service:CategoriaService=Depends(get_categoria_service)): return _translate(lambda: service.get(cid))
@router.post("",response_model=CategoriaRead,status_code=201)
def create(data:CategoriaCreate,_:Usuario=Depends(require_role(["admin"])),service:CategoriaService=Depends(get_categoria_service)): return _translate(lambda: service.create(data))
@router.put("/{cid}",response_model=CategoriaRead)
def update(cid:int,data:CategoriaUpdate,_:Usuario=Depends(require_role(["admin"])),service:CategoriaService=Depends(get_categoria_service)): return _translate(lambda: service.update(cid,data))
@router.delete("/{cid}",status_code=204)
def delete(cid:int,_:Usuario=Depends(require_role(["admin"])),service:CategoriaService=Depends(get_categoria_service)):
    _translate(lambda: service.deactivate(cid)); return Response(status_code=204)
