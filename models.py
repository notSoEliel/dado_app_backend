from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    contraseña = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.now)

    puntos = relationship("RegistroDePuntos", back_populates="usuario")

class RegistroDePuntos(Base):
    __tablename__ = "registro_de_puntos"
    id = Column(Integer, primary_key=True, index=True)
    cantidad_puntos = Column(Integer, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_registro = Column(DateTime, default=datetime.now)

    usuario = relationship("Usuario", back_populates="puntos")