from datetime import datetime, timezone
from sqlalchemy import func
from sqlmodel import select
from app.modules.pedidos.models import Pedido, DetallePedido
from app.modules.pedidos.schemas import PedidoCreate, PedidoRead, PedidosPaginados, ResumenPedidos
from app.modules.pedidos.unit_of_work import PedidoUnitOfWork

TRANSICIONES = {
    "PENDIENTE": {"EN_PREPARACION", "CANCELADO"},
    "EN_PREPARACION": {"ENTREGADO", "CANCELADO"},
    "ENTREGADO": set(),
    "CANCELADO": set(),
}

class PedidoError(Exception):
    status_code = 400
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)

class PedidoNoEncontrado(PedidoError):
    status_code = 404

class PedidoAjeno(PedidoError):
    status_code = 403

class ProductoPedidoNoEncontrado(PedidoError):
    status_code = 404

class PedidoReglaInvalida(PedidoError):
    status_code = 400

class PedidoService:
    def __init__(self, uow_factory=PedidoUnitOfWork):
        self.uow_factory = uow_factory

    def create(self, user_id: int, data: PedidoCreate) -> PedidoRead:
        ids = [item.producto_id for item in data.items]
        if len(ids) != len(set(ids)):
            raise PedidoReglaInvalida("Producto repetido")
        with self.uow_factory() as uow:
            pedido = Pedido(usuario_id=user_id, forma_pago=data.forma_pago,
                            direccion_entrega=data.direccion_entrega, notas=data.notas, total=0)
            uow.session.add(pedido)
            uow.session.flush()
            total = 0.0
            for item in data.items:
                producto = uow.productos.get_by_id_for_update(item.producto_id)
                if not producto or not producto.activo:
                    raise ProductoPedidoNoEncontrado("Producto inexistente o inactivo")
                if not producto.disponible:
                    raise PedidoReglaInvalida("Producto no disponible")
                if producto.stock < item.cantidad:
                    raise PedidoReglaInvalida("Stock insuficiente")
                producto.stock -= item.cantidad
                uow.session.add(producto)
                subtotal = producto.precio_base * item.cantidad
                total += subtotal
                uow.session.add(DetallePedido(
                    pedido_id=pedido.id, producto_id=producto.id, cantidad=item.cantidad,
                    nombre_producto=producto.nombre, precio_unitario=producto.precio_base,
                    subtotal=subtotal,
                ))
            pedido.total = total
            pedido.updated_at = datetime.now(timezone.utc)
            uow.session.add(pedido)
            uow.session.flush()
            return PedidoRead.model_validate(pedido)

    def list_orders(
        self, user_id: int, is_admin: bool, skip: int, limit: int,
        estado: str | None, own_only: bool = False,
    ) -> PedidosPaginados:
        with self.uow_factory() as uow:
            owner_id = None if is_admin and not own_only else user_id
            total, orders = uow.pedidos.list_orders(owner_id, skip, limit, estado)
            return PedidosPaginados(total=total, items=[PedidoRead.model_validate(order) for order in orders])

    def get(self, pedido_id: int, user_id: int, is_admin: bool) -> PedidoRead:
        with self.uow_factory() as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if not pedido:
                raise PedidoNoEncontrado("Pedido inexistente")
            if not is_admin and pedido.usuario_id != user_id:
                raise PedidoAjeno("Pedido ajeno")
            return PedidoRead.model_validate(pedido)

    def transition(self, pedido_id: int, new_state: str) -> PedidoRead:
        with self.uow_factory() as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if not pedido:
                raise PedidoNoEncontrado("Pedido inexistente")
            if new_state not in TRANSICIONES.get(pedido.estado, set()):
                raise PedidoReglaInvalida("Transición inválida")
            if new_state == "CANCELADO":
                self._restore_stock(uow, pedido)
            pedido.estado = new_state
            pedido.updated_at = datetime.now(timezone.utc)
            uow.session.add(pedido)
            uow.session.flush()
            return PedidoRead.model_validate(pedido)

    def cancel_for_user(self, pedido_id: int, user_id: int) -> PedidoRead:
        with self.uow_factory() as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if not pedido:
                raise PedidoNoEncontrado("Pedido inexistente")
            if pedido.usuario_id != user_id:
                raise PedidoAjeno("Pedido ajeno")
            if pedido.estado != "PENDIENTE":
                raise PedidoReglaInvalida("Solo se cancelan pedidos pendientes")
            self._restore_stock(uow, pedido)
            pedido.estado = "CANCELADO"
            pedido.updated_at = datetime.now(timezone.utc)
            uow.session.add(pedido)
            uow.session.flush()
            return PedidoRead.model_validate(pedido)

    @staticmethod
    def _restore_stock(uow, pedido: Pedido) -> None:
        for line in pedido.items:
            producto = uow.productos.get_by_id_for_update(line.producto_id)
            if producto:
                producto.stock += line.cantidad
                uow.session.add(producto)

    def summary(self) -> ResumenPedidos:
        with self.uow_factory() as uow:
            counts = {state: uow.pedidos.count_by_estado(state) for state in TRANSICIONES}
            today = datetime.now(timezone.utc).date()
            today_count = int(uow.session.exec(
                select(func.count()).select_from(Pedido).where(func.date(Pedido.created_at) == today)
            ).one())
            income = uow.session.exec(
                select(func.coalesce(func.sum(Pedido.total), 0)).where(Pedido.estado == "ENTREGADO")
            ).one()
            return ResumenPedidos(
                pendientes=counts["PENDIENTE"], en_preparacion=counts["EN_PREPARACION"],
                entregados=counts["ENTREGADO"], cancelados=counts["CANCELADO"],
                pedidos_hoy=today_count, ingresos_entregados=float(income or 0),
            )
