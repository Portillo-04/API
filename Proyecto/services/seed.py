from sqlmodel import Session, select
from config.db import engine
from models.evento import Local, Sala
from models.producto import Categoria
from models.usuario import Usuario, RolUsuario
from lib.pwd import get_password_hash


def seed_iniciales():
    """(S5) Carga datos iniciales obligatorios del TDR"""
    with Session(engine) as session:
        locales = session.exec(select(Local)).all()
        if not locales:
            sm = Local(nombre="San Miguel",
                       descripcion="Local amplio y cómodo, capacidad aprox. 150 personas.")
            lu = Local(
                nombre="La Unión", descripcion="Local amplio y cómodo, capacidad aprox. 150 personas.")
            session.add(sm)
            session.add(lu)
            session.commit()
            session.refresh(sm)
            session.refresh(lu)

            session.add_all([
                Sala(nombre="Sala 1", capacidad=150, local_id=sm.id),
                Sala(nombre="Sala 2", capacidad=150, local_id=sm.id),
                Sala(nombre="Sala 1", capacidad=150, local_id=lu.id),
                Sala(nombre="Sala 2", capacidad=150, local_id=lu.id),
            ])
            session.commit()

        categorias = session.exec(select(Categoria)).all()
        if not categorias:
            for nombre in ["Pasteles", "Postres", "Repostería", "Bebidas", "Otros productos"]:
                session.add(Categoria(nombre=nombre))
            session.commit()

        admin = session.exec(select(Usuario).where(
            Usuario.email == "admin@riospastries.com")).first()
        if not admin:
            session.add(Usuario(nombre="Administrador", email="admin@riospastries.com",
                        password=get_password_hash("admin123"), rol=RolUsuario.ADMINISTRADOR, activo=True))
            session.commit()
