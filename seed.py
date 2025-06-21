"""
seed.py

Este script inicializa la base de datos y precarga usuarios de ejemplo.
Se debe ejecutar una sola vez para poblar la tabla de usuarios.
"""

from database import (
    Base,
    engine,
    SessionLocal,
)  # Importa la base, el motor y la sesión de la base de datos
from models import Usuario  # Importa el modelo de usuario

# Crea todas las tablas definidas en los modelos (si no existen)
Base.metadata.create_all(bind=engine)


def cargar_usuarios():
    """
    Carga usuarios de ejemplo en la base de datos si aún no existen.
    Evita duplicados comprobando si ya hay usuarios registrados.
    """
    db = SessionLocal()

    if db.query(Usuario).first():
        print("⚠️ Usuarios ya existen. No se hará nada.")
        db.close()
        return

    usuarios = [
        Usuario(
            nombre_completo="Eliel García",
            username="neptune.son",
            contraseña="clave123",
        ),
        Usuario(
            nombre_completo="Angélica Rodríguez",
            username="thread.it",
            contraseña="clave231",
        ),
        Usuario(
            nombre_completo="Ericka Atencio",
            username="ericka_aves",
            contraseña="clave321",
        ),
    ]

    db.add_all(usuarios)  # Agrega todos los usuarios a la sesión
    db.commit()  # Guarda los cambios en la base de datos

    # Solo se crean los usuarios. Los puntos iniciales se asignan al iniciar sesión.

    db.close()
    print("✅ Usuarios precargados.")


if __name__ == "__main__":
    # Ejecuta la función para cargar usuarios solo si el script se ejecuta directamente
    cargar_usuarios()
