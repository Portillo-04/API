from sqlmodel import SQLModel, create_engine
from config.settings import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)


def crear_db_y_tablas():
    SQLModel.metadata.create_all(engine)
