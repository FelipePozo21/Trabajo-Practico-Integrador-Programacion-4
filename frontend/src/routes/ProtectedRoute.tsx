import type {ReactNode} from 'react';
import {Navigate} from 'react-router-dom';
import {useAuthStore} from '../store/authStore';
export function ProtectedRoute({role,children}:{role?:string;children:ReactNode}){
  const {user,loading}=useAuthStore();
  if(loading)return <div className="center">Verificando sesión…</div>;
  if(!user)return <Navigate to="/login" replace/>;
  if(role&&user.role!==role)return <Navigate to="/unauthorized" replace/>;
  return <>{children}</>;
}
