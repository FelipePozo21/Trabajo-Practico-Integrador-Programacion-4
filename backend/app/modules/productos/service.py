from app.core.domain_errors import NotFoundError
from app.modules.categorias.models import Categoria
from app.modules.productos.models import Producto
from app.modules.productos.schemas import ProductoCreate,ProductoUpdate,ProductoStockUpdate,ProductoRead,ProductosPaginados
from app.modules.productos.unit_of_work import ProductoUnitOfWork
class ProductoService:
    def __init__(self,uow_factory=ProductoUnitOfWork): self.uow_factory=uow_factory
    def list_active(self,skip=0,limit=20,search=None,categoria_id=None,disponible=None,solo_vendibles=False):
        with self.uow_factory() as uow:
            total,items=uow.productos.search(search,categoria_id,disponible,skip,min(limit,100),solo_vendibles)
            return ProductosPaginados(total=total,items=[ProductoRead.model_validate(p) for p in items])
    def get(self,pid:int,solo_vendibles:bool=False):
        with self.uow_factory() as uow:
            p=uow.productos.get_by_id(pid)
            if not p or not p.activo or (solo_vendibles and (not p.disponible or p.stock < 1)): raise NotFoundError("Producto inexistente")
            return ProductoRead.model_validate(p)
    def create(self,data:ProductoCreate):
        with self.uow_factory() as uow:
            c=uow.session.get(Categoria,data.categoria_id)
            if not c or not c.activo: raise NotFoundError("Categoría inexistente")
            return ProductoRead.model_validate(uow.productos.add(Producto(**data.model_dump())))
    def update(self,pid:int,data:ProductoUpdate):
        with self.uow_factory() as uow:
            p=uow.productos.get_by_id(pid)
            if not p or not p.activo: raise NotFoundError("Producto inexistente")
            values=data.model_dump(exclude_unset=True)
            if "categoria_id" in values:
                c=uow.session.get(Categoria,values["categoria_id"])
                if not c or not c.activo: raise NotFoundError("Categoría inexistente")
            for key,value in values.items(): setattr(p,key,value)
            uow.session.add(p);return ProductoRead.model_validate(p)
    def update_stock(self,pid:int,data:ProductoStockUpdate):
        with self.uow_factory() as uow:
            p=uow.productos.get_by_id(pid)
            if not p or not p.activo: raise NotFoundError("Producto inexistente")
            p.stock=data.stock;p.disponible=data.disponible;uow.session.add(p);return ProductoRead.model_validate(p)
    def deactivate(self,pid:int):
        with self.uow_factory() as uow:
            p=uow.productos.get_by_id(pid)
            if not p or not p.activo: raise NotFoundError("Producto inexistente")
            p.activo=False;uow.session.add(p)
