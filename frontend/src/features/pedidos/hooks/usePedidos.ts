import {useQuery} from '@tanstack/react-query';import {getOrders} from '../api/orders';
export function usePedidos(estado?:'PENDIENTE'|'EN_PREPARACION'|'ENTREGADO'|'CANCELADO'){return useQuery({queryKey:['pedidos',estado],queryFn:()=>getOrders({limit:100,estado})});}
