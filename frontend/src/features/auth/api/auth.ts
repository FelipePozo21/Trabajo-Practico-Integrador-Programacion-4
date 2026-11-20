import {api} from '../../../shared/api/axiosInstance';import type {User} from '../types/User';
export const getMe=async()=>(await api.get<User>('/auth/me')).data;
export const login=async(username:string,password:string)=>{const body=new URLSearchParams({username,password});await api.post('/auth/token',body,{headers:{'Content-Type':'application/x-www-form-urlencoded'}});return getMe();};
export const register=async(data:{username:string;full_name:string;email:string;password:string})=>(await api.post<User>('/auth/register',data)).data;
export const logout=()=>api.post('/auth/logout');
