from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.core.deps import get_session, get_current_active_user
from app.core.security import create_access_token
from app.core.config import settings
from app.modules.auth.service import AuthService
from app.modules.usuarios.schemas import UserCreate, UserPublic
from app.modules.usuarios.models import Usuario
router=APIRouter(prefix="/auth",tags=["autenticación"])
@router.post("/register",response_model=UserPublic,status_code=201)
def register(data:UserCreate, session:Session=Depends(get_session)): return AuthService(session).register(data)
@router.post("/token")
def login(response:Response,form:OAuth2PasswordRequestForm=Depends(),session:Session=Depends(get_session)):
    user=AuthService(session).authenticate(form.username,form.password)
    response.set_cookie("access_token",create_access_token(user.username),httponly=True,samesite="lax",secure=False,max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60)
    return {"message":"Login exitoso"}
@router.post("/logout")
def logout(response:Response): response.delete_cookie("access_token"); return {"message":"Sesión cerrada"}
@router.get("/me",response_model=UserPublic)
def me(user:Usuario=Depends(get_current_active_user)): return user
