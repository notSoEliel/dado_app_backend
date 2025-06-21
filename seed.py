from database import Base, engine, SessionLocal
from models import Usuario


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

    # Solo se crean los usuarios. Los puntos iniciales se asignan al iniciar sesión.

    db.close()
    print("✅ Usuarios precargados.")

if __name__ == "__main__":
    cargar_usuarios()