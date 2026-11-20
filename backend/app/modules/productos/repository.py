from sqlmodel import Session, select
from app.core.base_repository import BaseRepository
from app.modules.productos.models import Producto

class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def get_by_id_for_update(self, product_id: int) -> Producto | None:
        statement = select(Producto).where(Producto.id == product_id).with_for_update()
        return self.session.exec(statement).first()

    def search(self, search=None, categoria_id=None, disponible=None, skip=0, limit=20, solo_vendibles=False):
        query = select(Producto).where(Producto.activo == True)
        if search:
            query = query.where(Producto.nombre.ilike(f"%{search}%"))
        if categoria_id is not None:
            query = query.where(Producto.categoria_id == categoria_id)
        if disponible is not None:
            query = query.where(Producto.disponible == disponible)
        if solo_vendibles:
            query = query.where(Producto.disponible == True, Producto.stock > 0)
        total = len(self.session.exec(query).all())
        items = list(self.session.exec(query.offset(skip).limit(limit)).all())
        return total, items
