import {api} from '../../../shared/api/axiosInstance';import type {Category} from '../types/Category';
export const getCategories=async()=>(await api.get<Category[]>('/categorias')).data;
export const createCategory=async(data:Pick<Category,'nombre'|'descripcion'>)=>(await api.post<Category>('/categorias',data)).data;
export const updateCategory=async(id:number,data:Partial<Category>)=>(await api.put<Category>(`/categorias/${id}`,data)).data;
export const deleteCategory=async(id:number)=>api.delete(`/categorias/${id}`);
