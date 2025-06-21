"""
models.py

Este módulo define los modelos de la base de datos usando SQLAlchemy ORM.
Incluye las clases Usuario y RegistroDePuntos, que representan las tablas y sus relaciones.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)  # Importa tipos de columnas y claves foráneas
from sqlalchemy.orm import relationship  # Importa para definir relaciones entre tablas
from datetime import datetime  # Para manejar fechas y horas
from database import Base  # Importa la clase base para los modelos


class Usuario(Base):
    """
    Modelo que representa a un usuario en la base de datos.
    Atributos:
        - id: Identificador único del usuario.
        - nombre_completo: Nombre completo del usuario.
        - username: Nombre de usuario único para login.
        - contraseña: Contraseña del usuario.
        - fecha_registro: Fecha de creación del usuario.
        - puntos: Relación con los registros de puntos del usuario.
    """

    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    contraseña = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.now)

    puntos = relationship(
        "RegistroDePuntos", back_populates="usuario"
    )  # Relación uno a muchos


class RegistroDePuntos(Base):
    """
    Modelo que representa un registro de puntos asociado a un usuario.
    Atributos:
        - id: Identificador único del registro.
        - cantidad_puntos: Cantidad de puntos en este registro.
        - usuario_id: ID del usuario asociado.
        - fecha_registro: Fecha del registro de puntos.
        - usuario: Relación inversa con el usuario.
    """

    __tablename__ = "registro_de_puntos"
    id = Column(Integer, primary_key=True, index=True)
    cantidad_puntos = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_registro = Column(DateTime, default=datetime.now)

    usuario = relationship("Usuario", back_populates="puntos")  # Relación muchos a uno
