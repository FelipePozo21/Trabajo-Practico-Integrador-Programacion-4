from sqlalchemy import func
from sqlmodel import Session, select
from app.core.base_repository import BaseRepository
from app.modules.pedidos.models import Pedido

class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session):
        super().__init__(session, Pedido)

    def list_orders(self, usuario_id: int | None, skip: int, limit: int, estado: str | None):
        query = select(Pedido)
        count_query = select(func.count()).select_from(Pedido)
        if usuario_id is not None:
            query = query.where(Pedido.usuario_id == usuario_id)
            count_query = count_query.where(Pedido.usuario_id == usuario_id)
        if estado:
            query = query.where(Pedido.estado == estado)
            count_query = count_query.where(Pedido.estado == estado)
        total = int(self.session.exec(count_query).one())
        items = list(self.session.exec(query.order_by(Pedido.created_at.desc()).offset(skip).limit(limit)).all())
        return total, items

    def count_by_estado(self, estado: str) -> int:
        return int(self.session.exec(select(func.count()).select_from(Pedido).where(Pedido.estado == estado)).one())
