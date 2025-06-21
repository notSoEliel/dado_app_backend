from database import Base, engine, SessionLocal
from models import Usuario, RegistroDePuntos
from datetime import datetime

Base.metadata.create_all(bind=engine)

def cargar_usuarios():
    db = SessionLocal()

    if db.query(Usuario).first():
        print("⚠️ Usuarios ya existen. No se hará nada.")
        db.close()
        return

    usuarios = [
        Usuario(nombre_completo="Eliel García", username="neptune.son", contraseña="clave123"),
        Usuario(nombre_completo="Angélica Rodríguez", username="thread.it", contraseña="clave231"),
        Usuario(nombre_completo="Ericka Atencio", username="ericka_aves", contraseña="clave321"),
    ]

    db.add_all(usuarios)
    db.commit()

    # IMPORTANTE: Ahora que tienen ID, creamos registros de puntos
    for usuario in usuarios:
        registro = RegistroDePuntos(
            cantidad_puntos=1000,
            usuario_id=usuario.id,
            fecha_registro=datetime.utcnow()
        )
        db.add(registro)

    db.commit()
    db.close()
    print("✅ Usuarios y puntos iniciales cargados.")

if __name__ == "__main__":
    cargar_usuarios()