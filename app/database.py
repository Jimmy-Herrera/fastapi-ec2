from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./facturacion.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)


def crear_tablas():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session