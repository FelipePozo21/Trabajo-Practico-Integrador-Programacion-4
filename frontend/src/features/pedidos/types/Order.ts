export type OrderState='PENDIENTE'|'EN_PREPARACION'|'ENTREGADO'|'CANCELADO';
export interface OrderItem {producto_id:number;nombre_producto:string;precio_unitario:number;cantidad:number;subtotal:number}
export interface Order {id:number;usuario_id:number;estado:OrderState;forma_pago:'EFECTIVO'|'TRANSFERENCIA';direccion_entrega:string;notas:string|null;total:number;created_at:string;updated_at:string;items:OrderItem[]}
