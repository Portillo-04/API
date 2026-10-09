from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import get_settings
from config.db import crear_db_y_tablas
from services.seed import seed_iniciales
from routers import usuario_router, producto_router, pedido_router, evento_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_db_y_tablas()  # Crea las tablas en MySQL si no existen
    seed_iniciales()    # Carga locales, salas, categorías y admin
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Sistema Web para la Gestión de Pedidos y Eventos de Ríos Pastries (S1-S5)",
    lifespan=lifespan,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(usuario_router.router, tags=[
                   "S2: Usuarios y Autenticación"])
app.include_router(producto_router.router, tags=["S3: Catálogo y Productos"])
app.include_router(pedido_router.router, tags=["S4: Pedidos y Validaciones"])
app.include_router(evento_router.router, tags=["S5: Eventos y Reservaciones"])


@app.get("/status/negocio")
def business_status():
    from lib.utils import is_horario_atencion
    estado = "ABIERTO" if is_horario_atencion() else "CERRADO"
    mensaje = "Puede realizar pedidos en línea." if estado == "ABIERTO" else "Solo se permiten consultas y reservaciones de eventos."
    return {"estado": estado, "mensaje": mensaje}
