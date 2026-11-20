import {useQuery} from '@tanstack/react-query';import {getProducts} from '../api/products';import type {ProductFilters} from '../types/Product';
export function useProductos(filters:ProductFilters={}){return useQuery({queryKey:['productos',filters],queryFn:()=>getProducts(filters)});}
