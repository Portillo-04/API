from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from config.session_Dependencia import SessionDependencia
from config.permissions import RequireAdmin
from models.producto import Producto, ProductoCreate, ProductoUpdate, ProductoResponse, Categoria, CategoriaCreate, CategoriaResponse

router = APIRouter()


@router.get("/categorias", response_model=list[CategoriaResponse], summary="(S3) Consultar categorías")
def get_categorias(session: SessionDependencia):
    return session.exec(select(Categoria)).all()


@router.post("/categorias", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RequireAdmin)], summary="(S3) Crear categoría (Admin)")
def create_categoria(datos: CategoriaCreate, session: SessionDependencia):
    nueva = Categoria(**datos.model_dump())
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return CategoriaResponse.model_validate(nueva)


@router.get("/productos", response_model=list[ProductoResponse], summary="(S3) Consultar catálogo de productos")
def get_productos(session: SessionDependencia):
    return session.exec(select(Producto).where(Producto.disponible == True)).all()


@router.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RequireAdmin)], summary="(S3) Crear producto (Admin)")
def create_producto(datos: ProductoCreate, session: SessionDependencia):
    nuevo = Producto(**datos.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return ProductoResponse.model_validate(nuevo)
