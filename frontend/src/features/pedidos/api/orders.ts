import {api} from '../../../shared/api/axiosInstance';import type {Order,OrderState} from '../types/Order';
export const getOrders=async(params:{skip?:number;limit?:number;estado?:OrderState}={})=>(await api.get<{total:number;items:Order[]}>('/pedidos',{params})).data;
export const createOrder=async(data:{items:{producto_id:number;cantidad:number}[];forma_pago:'EFECTIVO'|'TRANSFERENCIA';direccion_entrega:string;notas?:string})=>(await api.post<Order>('/pedidos',data)).data;
export const changeOrderState=async(id:number,estado:OrderState)=>(await api.patch<Order>(`/pedidos/${id}/estado`,{estado})).data;
export const cancelOrder=async(id:number)=>(await api.patch<Order>(`/pedidos/${id}/cancelar`)).data;
export const getOrderSummary=async()=>(await api.get<{pendientes:number;en_preparacion:number;entregados:number;cancelados:number;pedidos_hoy:number;ingresos_entregados:number}>('/pedidos/resumen')).data;
