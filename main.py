"""
main.py

Este archivo define la API principal usando FastAPI.
Incluye endpoints para login, lanzar el dado y gestión de puntos.
Cada endpoint está documentado y comentado para facilitar la comprensión.
"""

from fastapi import FastAPI, Depends, HTTPException  # Framework para crear APIs
from pydantic import (
    BaseModel,
)  # Para validar y definir la estructura de los datos de entrada
from sqlalchemy.orm import Session  # Para manejar la sesión de la base de datos
from database import SessionLocal  # Importa la sesión local
import crud  # Importa las funciones CRUD personalizadas
from models import RegistroDePuntos  # Importa el modelo de registro de puntos
import random  # Para generar números aleatorios (simular el dado)
from datetime import datetime  # Para manejar fechas y horas

app = FastAPI()  # Crea la instancia principal de la aplicación


def get_db():
    """
    Proporciona una sesión de base de datos para cada petición.
    Se asegura de cerrar la sesión al finalizar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginRequest(BaseModel):
    """
    Modelo de datos para la petición de login.
    """

    username: str
    password: str


class PuntosRequest(BaseModel):
    """
    Modelo de datos para registrar puntos manualmente (no usado en los endpoints actuales).
    """

    usuario_id: int
    cantidad_puntos: int


@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint para autenticar a un usuario.
    Si es la primera vez que inicia sesión, se le asignan 1000 puntos iniciales.
    Devuelve el id, nombre completo y puntos actuales del usuario.
    """
    user = crud.autenticar_usuario(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Verificar si tiene puntos ya asignados
    puntos_existentes = (
        db.query(RegistroDePuntos)
        .filter(RegistroDePuntos.usuario_id == user.id)
        .order_by(RegistroDePuntos.fecha_registro.desc())
        .first()
    )

    if puntos_existentes is None:
        # Si es la primera vez, asigna 1000 puntos iniciales
        nuevo_registro = RegistroDePuntos(usuario_id=user.id, cantidad_puntos=1000)
        db.add(nuevo_registro)
        db.commit()

    # Obtener puntos actuales del último registro
    ultimo_registro = (
        db.query(RegistroDePuntos)
        .filter(RegistroDePuntos.usuario_id == user.id)
        .order_by(RegistroDePuntos.fecha_registro.desc())
        .first()
    )
    puntos_actuales = ultimo_registro.cantidad_puntos if ultimo_registro else 0

    return {
        "id": user.id,
        "nombre_completo": user.nombre_completo,
        "puntos": puntos_actuales,
    }


class LanzarDadoRequest(BaseModel):
    """
    Modelo de datos para la petición de lanzar el dado.
    """

    usuario_id: int


@app.post("/lanzar_dado")
def lanzar_dado(data: LanzarDadoRequest, db: Session = Depends(get_db)):
    """
    Endpoint para lanzar el dado.
    Resta 100 puntos al usuario por cada lanzamiento.
    Si el resultado es 6, suma 500 puntos.
    Devuelve el resultado del dado y los puntos actuales.
    """
    # Obtener último registro de puntos
    ultimo_registro = (
        db.query(RegistroDePuntos)
        .filter(RegistroDePuntos.usuario_id == data.usuario_id)
        .order_by(RegistroDePuntos.fecha_registro.desc())
        .first()
    )

    puntos_actuales = ultimo_registro.cantidad_puntos if ultimo_registro else 0

    if puntos_actuales < 100:  # type: ignore
        raise HTTPException(
            status_code=400, detail="No tienes suficientes puntos para lanzar el dado."
        )

    resultado = random.randint(1, 6)  # Simula el lanzamiento del dado
    nuevos_puntos = puntos_actuales - 100
    if resultado == 6:
        nuevos_puntos += 500  # Premio por sacar 6

    if ultimo_registro:
        ultimo_registro.cantidad_puntos = nuevos_puntos  # type: ignore
        ultimo_registro.fecha_registro = datetime.now()  # type: ignore
    db.commit()

    return {"resultado": resultado, "puntos_actuales": nuevos_puntos}
