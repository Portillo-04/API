from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session
from config.db import engine
from config.settings import settings
from models.usuario import Usuario, RolUsuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Credenciales inválidas")
    except JWTError:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    with Session(engine) as session:
        user = session.get(Usuario, user_id)
        if user is None:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado")
        return user


def RequireAutenticado(user: Usuario = Depends(get_current_user)):
    if not user.activo:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    return user


def RequireAdmin(user: Usuario = Depends(get_current_user)):
    if user.rol != RolUsuario.ADMINISTRADOR:
        raise HTTPException(
            status_code=403, detail="Permiso denegado: Se requiere rol de administrador")
    return user
