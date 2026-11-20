import {api} from '../../../shared/api/axiosInstance';import type {User} from '../../auth/types/User';
export const getUsers=async()=>(await api.get<User[]>('/admin/usuarios')).data;
export const setUserDisabled=(id:number,disabled:boolean)=>api.post<User>(`/admin/usuarios/${id}/${disabled?'desactivar':'activar'}`);
