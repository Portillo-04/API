from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List


class CategoriaBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=100)


class Categoria(CategoriaBase, table=True):
    __tablename__ = "categorias"
    id: int | None = Field(default=None, primary_key=True)
    productos: List["Producto"] = Relationship(back_populates="categoria")


class ProductoBase(SQLModel):
    nombre: str = Field(nullable=False, max_length=150)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    precio: float = Field(nullable=False, gt=0)
    imagen_url: Optional[str] = Field(default=None, max_length=255)
    categoria_id: int | None = Field(default=None, foreign_key="categorias.id")
    disponible: bool = Field(default=True)


class Producto(ProductoBase, table=True):
    __tablename__ = "productos"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    categoria: Optional[Categoria] = Relationship(back_populates="productos")


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    precio: Optional[float] = Field(default=None, gt=0)
    disponible: Optional[bool] = None


class ProductoResponse(ProductoBase):
    id: int
    created_at: datetime
    model_config = {"from_attributes": True}
