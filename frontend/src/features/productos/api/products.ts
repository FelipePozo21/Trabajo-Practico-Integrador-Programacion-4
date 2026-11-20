import {api} from '../../../shared/api/axiosInstance';import type {Product,ProductsPage,ProductFilters} from '../types/Product';
export const getProducts=async(filters:ProductFilters={})=>(await api.get<ProductsPage>('/productos',{params:filters})).data;
export const getProduct=async(id:number)=>(await api.get<Product>(`/productos/${id}`)).data;
export const createProduct=async(data:Omit<Product,'id'|'activo'|'categoria'>)=>(await api.post<Product>('/productos',data)).data;
export const updateProduct=async(id:number,data:Partial<Product>)=>(await api.put<Product>(`/productos/${id}`,data)).data;
export const updateProductStock=async(id:number,stock:number,disponible:boolean)=>(await api.patch<Product>(`/productos/${id}/stock`,{stock,disponible})).data;
export const deleteProduct=async(id:number)=>api.delete(`/productos/${id}`);
