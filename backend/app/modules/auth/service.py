from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy import func, or_
from app.modules.usuarios.models import Usuario
from app.modules.usuarios.schemas import UserCreate
from app.core.security import hash_password, verify_password
class AuthService:
    def __init__(self, session: Session): self.session=session
    def register(self, data: UserCreate):
        if self.session.exec(select(Usuario).where((Usuario.username==data.username)|(Usuario.email==data.email))).first(): raise HTTPException(409,"Username o email ya registrado")
        user=Usuario(username=data.username,full_name=data.full_name,email=data.email,hashed_password=hash_password(data.password),role="user")
        self.session.add(user); self.session.commit(); self.session.refresh(user); return user
    def authenticate(self, username, password):
        user=self.session.exec(select(Usuario).where(or_(Usuario.username==username,func.lower(Usuario.email)==username.lower()))).first()
        if not user or not verify_password(password,user.hashed_password): raise HTTPException(401,"Credenciales incorrectas")
        if user.disabled: raise HTTPException(400,"Cuenta de usuario desactivada")
        return user
