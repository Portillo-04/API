from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import sqlalchemy as sa
from pydantic import EmailStr


class RolUsuario(str, Enum):
    CLIENTE = "cliente"
    ADMINISTRADOR = "administrador"


class UsuarioBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=100, min_length=3)
    email: EmailStr = Field(nullable=False, max_length=150)
    rol: RolUsuario = Field(default=RolUsuario.CLIENTE, sa_column=sa.Column(
        sa.String(20), nullable=False, server_default="cliente"))


class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"
    id: int | None = Field(default=None, primary_key=True)
    password: str = Field(nullable=False, max_length=255)
    activo: bool = Field(default=True)
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class UsuarioCreate(UsuarioBase):
    password: str = Field(nullable=False, max_length=255, min_length=6)


class UsuarioUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=100, min_length=3)
    email: Optional[EmailStr] = Field(default=None, max_length=150)
    password: Optional[str] = Field(default=None, max_length=255, min_length=6)
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    created_at: datetime
    model_config = {"from_attributes": True}
