"""
database.py

Este módulo configura la conexión a la base de datos usando SQLAlchemy.
Define el motor de la base de datos, la sesión y la clase base para los modelos ORM.
"""

from sqlalchemy import (
    create_engine,
)  # Importa la función para crear el motor de la base de datos
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
)  # Importa utilidades para sesiones y modelos

# URL de la base de datos SQLite. El archivo dado_app.db se creará/localizará en el mismo directorio.
DATABASE_URL = "sqlite:///./dado_app.db"

# Crea el motor de la base de datos. 'check_same_thread' es necesario para SQLite en aplicaciones multihilo.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crea una clase SessionLocal que se usará para crear sesiones de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos ORM. Todos los modelos deben heredar de esta clase.
Base = declarative_base()
