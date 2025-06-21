# Backend - FastAPI (Login y Registro de Puntos)

Este backend provee una API REST construida con **FastAPI**, conectada a una base de datos **SQLite**. Proporciona autenticación simple (sin registro) y permite guardar puntos asociados a usuarios preexistentes.

---

## 🚀 Endpoints Disponibles

### `POST /login`

Autenticación básica de usuario con username y contraseña.

**Request Body:**

```json
{
  "username": "neptune.son",
  "password": "clave123"
}

Response (éxito):

{
  "id": 1,
  "nombre_completo": "Eliel García"
}

```

---

### `POST /registro_de_puntos`

Registra un puntaje para un usuario dado.

**Request Body:**

```json
{
  "usuario_id": 1,
  "cantidad_puntos": 1000
}
```

---

## 📦 Estructura del Proyecto

```markdown
backend/
├── main.py            # Entrypoint de FastAPI
├── database.py        # Conexión SQLite + Session
├── models.py          # Modelos ORM con SQLAlchemy
├── crud.py            # Lógica de negocio (login, registrar puntos)
├── seed.py            # Precarga de usuarios

```

---

## 🔧 Cómo Ejecutar

### 1. Instalar dependencias:

```bash
pip install uv
uv add fastapi uvicorn sqlalchemy
```

### 2. Crear la base de datos y precargar usuarios:

```bash
uv run seed.py
```

### 3. Ejecutar el servidor:

```bash
uv run uvicorn main:app --reload
```

---

## 📝 Usuarios Predefinidos

 • neptune.son / clave123
 • thread.it / clave231
 • ericka_aves / clave321


