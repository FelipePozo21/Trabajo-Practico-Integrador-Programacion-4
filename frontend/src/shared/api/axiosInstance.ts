import axios from 'axios';
export const api = axios.create({baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',withCredentials:true});
function validationDetails(detail:unknown):string|undefined{
  if(!Array.isArray(detail))return undefined;
  const labels:Record<string,string>={username:'Usuario',full_name:'Nombre completo',email:'Email',password:'Contraseña'};
  const messages=detail.map((entry:unknown)=>{
    if(typeof entry!=='object'||entry===null)return String(entry);
    const issue=entry as {loc?:unknown[];msg?:unknown};
    const field=Array.isArray(issue.loc)?issue.loc.map(String).filter(part=>part!=='body').map(part=>labels[part]??part).join(' → '):'Formulario';
    return `${field}: ${typeof issue.msg==='string'?issue.msg:'dato inválido'}`;
  });
  return messages.length?messages.join('. '):undefined;
}
export function errorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail:unknown=error.response?.data?.detail;
    if(typeof detail==='string')return detail;
    const validation=validationDetails(detail);
    if(validation)return validation;
    return 'No se pudo completar la operación.';
  }
  return 'Ocurrió un error inesperado.';
}
api.interceptors.response.use(response=>response,async error=>{const status=error.response?.status;const detail=error.response?.data?.detail;const url=String(error.config?.url||'');const expired=status===401&&!url.includes('/auth/token')&&!url.includes('/auth/me');const disabled=status===400&&detail==='Cuenta de usuario desactivada';if(expired||disabled){const {useAuthStore}=await import('../../store/authStore');useAuthStore.getState().setUser(null);if(typeof window!=='undefined'&&!window.location.pathname.startsWith('/login'))window.location.assign('/login');}return Promise.reject(error)});
