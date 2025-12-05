# 🔌 Backend - API REST del Sistema Escolar

## 📋 Descripción

API REST desarrollada con **Django** y **Django REST Framework** que proporciona todos los servicios necesarios para la gestión de la aplicación de Sistema Escolar. Esta API maneja autenticación, gestión de usuarios, estudiantes, maestros, eventos académicos y estadísticas.

## 🎯 Endpoints Principales

### Autenticación
```
POST   /api/auth/login/           - Iniciar sesión
POST   /api/auth/logout/          - Cerrar sesión
POST   /api/auth/refresh-token/   - Renovar token
GET    /api/auth/user/            - Obtener usuario actual
```

### Administradores
```
GET    /api/administradores/      - Listar administradores
POST   /api/administradores/      - Crear administrador
GET    /api/administradores/{id}/ - Obtener administrador
PUT    /api/administradores/{id}/ - Actualizar administrador
DELETE /api/administradores/{id}/ - Eliminar administrador
```

### Maestros
```
GET    /api/maestros/             - Listar maestros
POST   /api/maestros/             - Crear maestro
GET    /api/maestros/{id}/        - Obtener maestro
PUT    /api/maestros/{id}/        - Actualizar maestro
DELETE /api/maestros/{id}/        - Eliminar maestro
```

### Alumnos
```
GET    /api/alumnos/              - Listar estudiantes
POST   /api/alumnos/              - Crear estudiante
GET    /api/alumnos/{id}/         - Obtener estudiante
PUT    /api/alumnos/{id}/         - Actualizar estudiante
DELETE /api/alumnos/{id}/         - Eliminar estudiante
```

### Eventos Académicos
```
GET    /api/eventos/              - Listar eventos
POST   /api/eventos/              - Crear evento
GET    /api/eventos/{id}/         - Obtener evento
PUT    /api/eventos/{id}/         - Actualizar evento
DELETE /api/eventos/{id}/         - Eliminar evento
GET    /api/eventos/estadisticas/ - Obtener estadísticas
```

## 🏗️ Estructura de Archivos

```
dev_sistema_escolar_api/
├── dev_sistema_escolar_api/
│   ├── __init__.py
│   ├── settings.py              # Configuración de Django
│   ├── urls.py                  # Rutas principales
│   ├── wsgi.py                  # Punto de entrada WSGI
│   ├── models.py                # Modelos de datos
│   ├── serializers.py           # Serializadores DRF
│   ├── admin.py                 # Configuración admin
│   ├── utils.py                 # Funciones utilitarias
│   ├── data_utils.py            # Utilidades de datos
│   ├── cypher_utils.py          # Encriptación
│   └── views/
│       ├── __init__.py
│       ├── auth.py              # Vistas de autenticación
│       ├── alumnos.py           # Vistas de estudiantes
│       ├── maestros.py          # Vistas de maestros
│       ├── users.py             # Vistas de usuarios
│       ├── eventos.py           # Vistas de eventos
│       └── bootstrap.py         # Inicialización de datos
├── migrations/                  # Migraciones de BD
├── puentes/
│   └── mail.py                  # Servicio de correo
├── static/                      # Archivos estáticos
├── manage.py                    # Gestor de Django
├── requirements.txt             # Dependencias Python
├── my.cnf                       # Configuración MySQL
├── app.yaml                     # Configuración App Engine
└── deploy.sh                    # Script de despliegue
```

## 🗄️ Modelos de Datos

### Administradores
```python
class Administradores(models.Model):
    nombre = CharField(max_length=100)
    apellidos = CharField(max_length=100)
    correo = EmailField(unique=True)
    contraseña = CharField(max_length=255)
    telefono = CharField(max_length=20)
    direccion = TextField()
    activo = BooleanField(default=True)
    update = DateTimeField(auto_now=True)
    created = DateTimeField(auto_now_add=True)
```

### Maestros
```python
class Maestros(models.Model):
    nombre = CharField(max_length=100)
    apellidos = CharField(max_length=100)
    numero_empleado = CharField(max_length=50, unique=True)
    correo = EmailField(unique=True)
    contraseña = CharField(max_length=255)
    departamento = CharField(max_length=100)
    especialidad = CharField(max_length=100)
    telefono = CharField(max_length=20)
    estado = BooleanField(default=True)
    update = DateTimeField(auto_now=True)
    created = DateTimeField(auto_now_add=True)
```

### Alumnos
```python
class Alumnos(models.Model):
    nombre = CharField(max_length=100)
    apellidos = CharField(max_length=100)
    matricula = CharField(max_length=50, unique=True)
    correo = EmailField(unique=True)
    contraseña = CharField(max_length=255)
    fecha_nacimiento = DateField()
    grado = CharField(max_length=50)
    grupo = CharField(max_length=10)
    telefono = CharField(max_length=20)
    direccion = TextField()
    estado = BooleanField(default=True)
    update = DateTimeField(auto_now=True)
    created = DateTimeField(auto_now_add=True)
```

### Eventos Académicos
```python
class EventosAcademicos(models.Model):
    titulo = CharField(max_length=200)
    descripcion = TextField()
    tipo = CharField(max_length=100)
    fecha = DateField()
    hora = TimeField()
    ubicacion = CharField(max_length=255)
    publico_objetivo = CharField(max_length=255)
    estado = BooleanField(default=True)
    update = DateTimeField(auto_now=True)
    created = DateTimeField(auto_now_add=True)
```

## 🚀 Instalación y Configuración

### Requisitos
- Python 3.8+
- pip
- MySQL 5.7+ o MariaDB
- Virtual Environment

### Pasos de Instalación

```bash
# 1. Navegar al directorio
cd dev_sistema_escolar_api

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos en settings.py
# Editar DATABASES con credenciales MySQL

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Cargar datos iniciales (opcional)
python manage.py bootstrap

# 8. Ejecutar servidor
python manage.py runserver
```

## 📦 Dependencias Principales

```
Django==4.2
djangorestframework==3.14
django-cors-headers==4.0
Pillow==9.5
mysqlclient==2.1
python-decouple==3.8
PyJWT==2.8
```

Ver `requirements.txt` para la lista completa.

## 🔐 Autenticación

La API utiliza autenticación basada en **JWT (JSON Web Tokens)**:

```python
# Request
POST /api/auth/login/
{
    "usuario": "admin",
    "contraseña": "password123"
}

# Response
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "nombre": "Admin",
        "tipo": "administrador"
    }
}
```

Incluir el token en el header para requests autenticados:
```
Authorization: Bearer {token}
```

## 🔒 Seguridad

- ✅ Contraseñas encriptadas con hashing seguro
- ✅ CORS habilitado para dominios permitidos
- ✅ Validación de entrada en todos los endpoints
- ✅ Rate limiting en endpoints sensibles
- ✅ Tokens JWT con expiración
- ✅ Sanitización de datos

## 📊 Endpoints de Estadísticas

```python
GET /api/eventos/estadisticas/

Response:
{
    "total_eventos": 25,
    "eventos_por_tipo": {
        "Conferencia": 8,
        "Taller": 10,
        "Seminario": 7
    },
    "eventos_por_mes": {
        "2025-12": 15,
        "2025-11": 10
    }
}
```

# dev_sistema_escolar_api
