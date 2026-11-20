import {useMutation,useQueryClient} from '@tanstack/react-query';
import {cancelOrder,changeOrderState,createOrder} from '../api/orders';
import type {OrderState} from '../types/Order';
export function useCrearPedido(){const client=useQueryClient();return useMutation({mutationFn:createOrder,onSuccess:()=>client.invalidateQueries({queryKey:['pedidos']})});}
export function useCambiarEstadoPedido(){const client=useQueryClient();return useMutation({mutationFn:({id,estado}:{id:number;estado:OrderState})=>changeOrderState(id,estado),onSuccess:()=>{void client.invalidateQueries({queryKey:['pedidos']});void client.invalidateQueries({queryKey:['resumen']});}});}
export function useCancelarPedido(){const client=useQueryClient();return useMutation({mutationFn:cancelOrder,onSuccess:()=>{void client.invalidateQueries({queryKey:['pedidos']});void client.invalidateQueries({queryKey:['resumen']});}});}
