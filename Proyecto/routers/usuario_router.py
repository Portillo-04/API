from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from config.session_Dependencia import SessionDependencia
from config.permissions import RequireAutenticado, get_current_user
from lib.pwd import get_password_hash, verify_password
from lib.utils import generar_codigo_recuperacion
from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse, RolUsuario
from config.security import create_access_token
from datetime import datetime, timezone

router = APIRouter()


@router.post("/usuarios/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="(S2) Registrar Cliente")
def register_usuario(datos: UsuarioCreate, session: SessionDependencia):
    if session.exec(select(Usuario).where(Usuario.email == datos.email)).first():
        raise HTTPException(
            status_code=400, detail="El email ya está registrado")
    nuevo = Usuario(**datos.model_dump(exclude={'password'}),
                    password=get_password_hash(datos.password), activo=True)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return UsuarioResponse.model_validate(nuevo)


@router.post("/usuarios/login", summary="(S2) Iniciar Sesión")
def login(session: SessionDependencia, form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = session.exec(select(Usuario).where(
        Usuario.email == form_data.username)).first()
    if not usuario or not verify_password(form_data.password, usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if not usuario.activo:
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    token = create_access_token(
        data={"sub": usuario.email, "id": usuario.id, "rol": usuario.rol})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/usuarios/me", response_model=UsuarioResponse, dependencies=[Depends(RequireAutenticado)], summary="(S2) Obtener mi perfil")
def get_me(usuario: Usuario = Depends(get_current_user)):
    return UsuarioResponse.model_validate(usuario)


@router.post("/usuarios/forgot-password", summary="(S2) Recuperar Contraseña")
def forgot_password(email: str, session: SessionDependencia):
    usuario = session.exec(select(Usuario).where(
        Usuario.email == email)).first()
    if usuario:
        codigo = generar_codigo_recuperacion()
        print(f"[SIMULACIÓN] Código de recuperación para {email}: {codigo}")
    return {"message": "Si el correo existe, se ha enviado un código de recuperación."}
