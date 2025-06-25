# Backend - FastAPI (Login y Registro de Puntos)

Este backend provee una API REST construida con **FastAPI**, conectada a una base de datos **SQLite**. Proporciona autenticación simple (sin registro) y permite guardar puntos asociados a usuarios preexistentes. El puntaje se asigna solo la primera vez que el usuario inicia sesión y se actualiza directamente (no se crean múltiples registros).

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
  "nombre_completo": "Eliel García",
  "puntos": 1000
}

```

---

### `POST /lanzar_dado`

Realiza un lanzamiento de dado. Resta 100 puntos. Si el resultado es 6, suma 500.

**Request Body:**
```json
{
  "usuario_id": 1
}
```

**Response:**
```json
{
  "resultado": 4,
  "puntos_actuales": 900
}
```

---

### `GET /obtener_puntos`

Obtiene los puntos actuales de un usuario.

**Parámetros de consulta:**
- `usuario_id` (int): ID del usuario a consultar.

**Ejemplo de request:**
```
GET /obtener_puntos?usuario_id=1
```

**Response:**
```json
{
  "usuario_id": 1,
  "puntos_actuales": 900
}
```

---

## 📦 Estructura del Proyecto

```markdown
backend/
├── main.py            # Entrypoint de FastAPI
├── database.py        # Conexión SQLite + Session
├── models.py          # Modelos ORM con SQLAlchemy
├── crud.py            # Lógica de negocio (login, lanzar dado)
├── seed.py            # Precarga de usuarios

```

---

## 🔧 Cómo Ejecutar

### 1. Instalar dependencias:

```bash
pip install uv
uv sync
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


