from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.deps import get_session, require_role
from app.modules.usuarios.models import Usuario
from app.modules.usuarios.schemas import UserPublic
router=APIRouter(prefix="/admin/usuarios",tags=["usuarios"])
@router.get("",response_model=list[UserPublic])
def list_users(session:Session=Depends(get_session),_:Usuario=Depends(require_role(["admin"]))): return session.exec(select(Usuario)).all()
def change(uid:int,disabled:bool,session:Session,actor:Usuario):
    user=session.get(Usuario,uid)
    if not user: raise HTTPException(404,"Usuario inexistente")
    if user.id==actor.id and disabled: raise HTTPException(400,"No puede desactivarse a sí mismo")
    user.disabled=disabled; session.add(user);session.commit();session.refresh(user);return user
@router.post("/{uid}/activar",response_model=UserPublic)
def activate(uid:int,session:Session=Depends(get_session),actor:Usuario=Depends(require_role(["admin"]))): return change(uid,False,session,actor)
@router.post("/{uid}/desactivar",response_model=UserPublic)
def deactivate(uid:int,session:Session=Depends(get_session),actor:Usuario=Depends(require_role(["admin"]))): return change(uid,True,session,actor)
