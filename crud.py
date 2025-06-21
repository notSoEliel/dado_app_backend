from sqlalchemy.orm import Session
from models import Usuario, RegistroDePuntos

def autenticar_usuario(db: Session, username: str, password: str):
    return db.query(Usuario).filter(Usuario.username == username, Usuario.contraseña == password).first()

def registrar_puntos(db: Session, usuario_id: int, cantidad: int):
    registro = RegistroDePuntos(usuario_id=usuario_id, cantidad_puntos=cantidad)
    db.add(registro)
    db.commit()
    db.refresh(registro)
    return registro