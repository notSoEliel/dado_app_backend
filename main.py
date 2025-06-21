from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
from models import RegistroDePuntos
import random
from datetime import datetime

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginRequest(BaseModel):
    username: str
    password: str


class PuntosRequest(BaseModel):
    usuario_id: int
    cantidad_puntos: int


@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
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
    usuario_id: int


@app.post("/lanzar_dado")
def lanzar_dado(data: LanzarDadoRequest, db: Session = Depends(get_db)):
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

    resultado = random.randint(1, 6)
    nuevos_puntos = puntos_actuales - 100
    if resultado == 6:
        nuevos_puntos += 500

    if ultimo_registro:
        ultimo_registro.cantidad_puntos = nuevos_puntos  # type: ignore
        ultimo_registro.fecha_registro = datetime.now()  # type: ignore
    db.commit()

    return {"resultado": resultado, "puntos_actuales": nuevos_puntos}
