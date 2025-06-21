"""
crud.py

Este módulo contiene funciones para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) relacionadas con los usuarios y el registro de puntos en la base de datos.

Funciones:
- autenticar_usuario: Verifica si un usuario existe con el username y contraseña proporcionados.
- registrar_puntos: Registra una cantidad de puntos para un usuario específico.
"""

from sqlalchemy.orm import (
    Session,
)  # Importa la clase Session para manejar la conexión a la base de datos
from models import Usuario, RegistroDePuntos  # Importa los modelos de la base de datos


def autenticar_usuario(db: Session, username: str, password: str):
    """
    Autentica a un usuario verificando su username y contraseña.

    Args:
        db (Session): Sesión de la base de datos.
        username (str): Nombre de usuario.
        password (str): Contraseña del usuario.

    Returns:
        Usuario: El objeto Usuario si las credenciales son correctas, None si no lo son.
    """
    # Busca un usuario que coincida con el username y la contraseña proporcionados
    return (
        db.query(Usuario)
        .filter(Usuario.username == username, Usuario.contraseña == password)
        .first()
    )


def registrar_puntos(db: Session, usuario_id: int, cantidad: int):
    """
    Registra una nueva entrada de puntos para un usuario específico.

    Args:
        db (Session): Sesión de la base de datos.
        usuario_id (int): ID del usuario al que se le asignarán los puntos.
        cantidad (int): Cantidad de puntos a registrar.

    Returns:
        RegistroDePuntos: El objeto de registro de puntos recién creado.
    """
    # Crea un nuevo registro de puntos para el usuario
    registro = RegistroDePuntos(usuario_id=usuario_id, cantidad_puntos=cantidad)
    db.add(registro)  # Agrega el registro a la sesión
    db.commit()  # Guarda los cambios en la base de datos
    db.refresh(registro)  # Actualiza el objeto con los datos guardados
    return registro
