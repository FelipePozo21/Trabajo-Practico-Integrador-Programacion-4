from fastapi import Depends, HTTPException, Request
from sqlmodel import Session, select
from app.core.database import session_factory
from app.core.security import decode_access_token
from app.modules.usuarios.models import Usuario

def get_session():
    with session_factory() as session: yield session

def get_current_user(request: Request, session: Session = Depends(get_session)) -> Usuario:
    subject = decode_access_token(request.cookies.get("access_token", ""))
    if not subject: raise HTTPException(401, "Sesión inválida o vencida")
    user = session.exec(select(Usuario).where(Usuario.username == subject)).first()
    if not user: raise HTTPException(401, "Usuario inexistente")
    return user

def get_current_active_user(user: Usuario = Depends(get_current_user)) -> Usuario:
    if user.disabled: raise HTTPException(400, "Cuenta de usuario desactivada")
    return user

def require_role(roles: list[str]):
    def check(user: Usuario = Depends(get_current_active_user)):
        if user.role not in roles: raise HTTPException(403, "Rol no permitido")
        return user
    return check
