# EduTrack — Gestión de Estudiantes

Aplicación web desarrollada con **Python + Flask** para registrar y administrar el rendimiento académico de estudiantes.

## Descripción

EduTrack permite llevar un registro de estudiantes con nombre, carrera y nota. Incluye estadísticas en tiempo real (total, promedio y mejor nota), búsqueda, y una API REST completa.

---

## Estructura del proyecto

```
Tarea3.0/
├── app.py                               # Aplicación Flask principal
├── test_app.py                          # Pruebas automatizadas (pytest)
├── requirements.txt                     # Dependencias Python
├── Dockerfile                           # Imagen Docker
├── README.md                            # Este archivo
└── .github/
    └── workflows/
        └── python-application.yml       # Pipeline CI/CD
```

---

## Requisitos

- Python 3.12
- pip
- Docker (opcional)

---

## Instalación y ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/andernarvaez05/Tarea3.0.git
cd Tarea3.0

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python app.py
```

La aplicación queda disponible en: **http://localhost:5000**

---

## Pruebas automatizadas

```bash
pytest test_app.py -v
```

| # | Test | Descripción |
|---|------|-------------|
| 1 | `test_home_page_loads` | La página principal responde con código 200 |
| 2 | `test_get_students_returns_list` | `GET /api/students` retorna una lista JSON |
| 3 | `test_add_student_valid` | Agrega un estudiante con datos válidos (201) |
| 4 | `test_add_student_invalid_grade` | Rechaza una nota mayor a 10 (400) |
| 5 | `test_add_student_missing_name` | Rechaza nombre vacío (400) |
| 6 | `test_delete_student` | Elimina un estudiante existente (200) |
| 7 | `test_delete_nonexistent_student` | Retorna 404 si el ID no existe |
| 8 | `test_search_by_name` | La búsqueda filtra correctamente por nombre |

---

## Docker

```bash
# Construir la imagen
docker build -t ejercicio:3.0.0 .

# Ejecutar el contenedor (el -p 5000:5000 expone el puerto al navegador)
docker run -p 5000:5000 ejercicio:3.0.0
```

Luego abrir en el navegador: **http://localhost:5000**

> ⚠️ Sin `-p 5000:5000` el contenedor corre internamente pero no es accesible desde el navegador.

Imagen publicada en GitHub Container Registry:

```bash
docker pull ghcr.io/andernarvaez05/ejercicio:3.0.0
docker run -p 5000:5000 ghcr.io/andernarvaez05/ejercicio:3.0.0
```

---

## API REST

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Interfaz web |
| `GET` | `/api/students` | Lista todos los estudiantes |
| `GET` | `/api/students?q=texto` | Filtra por nombre o carrera |
| `POST` | `/api/students` | Agrega un estudiante |
| `DELETE` | `/api/students/<id>` | Elimina un estudiante |


---

## CI/CD — GitHub Actions

El archivo `.github/workflows/python-application.yml` se ejecuta automáticamente en cada `push` a la rama `main` y realiza los siguientes pasos:

| Paso | Nombre | Descripción |
|------|--------|-------------|
| 1 | Descargar código fuente | `actions/checkout@v4` |
| 2 | Configurar Python 3.12 | `actions/setup-python@v5` |
| 3 | Instalar dependencias | `pip install -r requirements.txt` |
| 4 | Ejecutar pruebas con pytest | `pytest test_app.py -v` |
| 5 | Ejecutar la aplicación | Levanta el servidor y verifica con `curl` |
| 6 | Simular despliegue | Muestra mensajes de confirmación |
| 7 | Construir imagen Docker | `docker build` con tag `ejercicio:3.0.0` |
| 8 | Login en GHCR | Autenticación con `GITHUB_TOKEN` |
| 9 | Publicar imagen | `docker push` a `ghcr.io/andernarvaez05/ejercicio:3.0.0` |

---

**Tarea 3.0**  Anderson Narváez