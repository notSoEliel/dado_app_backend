from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
import crud

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
    return {"id": user.id, "nombre_completo": user.nombre_completo}

@app.post("/registro_de_puntos")
def registrar_puntos(data: PuntosRequest, db: Session = Depends(get_db)):
    registro = crud.registrar_puntos(db, data.usuario_id, data.cantidad_puntos)
    return {"mensaje": "Puntos registrados", "id": registro.id}