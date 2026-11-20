from app.core.domain_errors import NotFoundError, ConflictError
from sqlmodel import select
from app.modules.categorias.models import Categoria
from app.modules.categorias.schemas import CategoriaCreate, CategoriaUpdate, CategoriaRead
from app.modules.categorias.unit_of_work import CategoriaUnitOfWork

class CategoriaService:
    def __init__(self, uow_factory=CategoriaUnitOfWork): self.uow_factory=uow_factory
    def list_active(self):
        with self.uow_factory() as uow:
            return [CategoriaRead.model_validate(x) for x in uow.session.exec(select(Categoria).where(Categoria.activo==True)).all()]
    def get(self,cid:int):
        with self.uow_factory() as uow:
            obj=uow.categorias.get_by_id(cid)
            if not obj or not obj.activo: raise NotFoundError("Categoría inexistente")
            return CategoriaRead.model_validate(obj)
    def create(self,data:CategoriaCreate):
        with self.uow_factory() as uow:
            if uow.session.exec(select(Categoria).where(Categoria.nombre==data.nombre)).first(): raise ConflictError("Nombre duplicado")
            obj=uow.categorias.add(Categoria(**data.model_dump()))
            return CategoriaRead.model_validate(obj)
    def update(self,cid:int,data:CategoriaUpdate):
        with self.uow_factory() as uow:
            obj=uow.categorias.get_by_id(cid)
            if not obj or not obj.activo: raise NotFoundError("Categoría inexistente")
            changes=data.model_dump(exclude_unset=True)
            if "nombre" in changes and uow.session.exec(select(Categoria).where(Categoria.nombre==changes["nombre"],Categoria.id!=cid)).first(): raise ConflictError("Nombre duplicado")
            for key,value in changes.items(): setattr(obj,key,value)
            uow.session.add(obj); return CategoriaRead.model_validate(obj)
    def deactivate(self,cid:int):
        with self.uow_factory() as uow:
            obj=uow.categorias.get_by_id(cid)
            if not obj or not obj.activo: raise NotFoundError("Categoría inexistente")
            obj.activo=False;uow.session.add(obj)
