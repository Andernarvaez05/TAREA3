# EduTrack — Gestión de Estudiantes

Aplicación web sencilla construida con **Flask** (Python) para registrar y administrar el rendimiento académico de estudiantes.

## Funcionalidades

- Listar estudiantes con nombre, carrera y nota
- Agregar nuevos estudiantes mediante formulario
- Eliminar estudiantes
- Buscador en tiempo real por nombre o carrera
- Estadísticas: total, promedio y mejor nota
- API REST JSON

---

## Requisitos previos

- Python 3.12+
- pip
- Docker (opcional)

---

## Ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/andernarvaez05/Tarea3.0.git
cd Tarea3.0

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

---

## Pruebas automatizadas

```bash
pytest test_app.py -v
```

Se ejecutan **8 casos de prueba** que cubren:

| Test | Descripción |
|------|-------------|
| `test_home_page_loads` | La página principal responde 200 |
| `test_get_students_returns_list` | `GET /api/students` retorna lista JSON |
| `test_add_student_valid` | Agrega estudiante con datos correctos (201) |
| `test_add_student_invalid_grade` | Nota > 10 es rechazada (400) |
| `test_add_student_missing_name` | Nombre vacío es rechazado (400) |
| `test_delete_student` | Elimina estudiante existente (200) |
| `test_delete_nonexistent_student` | ID inexistente devuelve 404 |
| `test_search_by_name` | Búsqueda filtra correctamente |

---

## Ejecución con Docker

```bash
# Construir la imagen
docker build -t ejercicio:3.0.0 .

# Ejecutar el contenedor
docker run -p 5000:5000 ejercicio:3.0.0
```

O usar la imagen publicada en GitHub Container Registry:

```bash
docker pull ghcr.io/andernarvaez05/ejercicio:3.0.0
docker run -p 5000:5000 ghcr.io/andernarvaez05/ejercicio:3.0.0
```

---

## API REST

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Interfaz web principal |
| `GET` | `/api/students` | Lista todos los estudiantes |
| `GET` | `/api/students?q=texto` | Filtra por nombre o carrera |
| `POST` | `/api/students` | Agrega un estudiante |
| `DELETE` | `/api/students/<id>` | Elimina un estudiante |

### Ejemplo POST

```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name": "María López", "grade": 8.5, "career": "Ingeniería"}'
```

---

## CI/CD — GitHub Actions

El workflow `.github/workflows/python-application.yml` se ejecuta en cada push a `main` y realiza:

1. Descarga el código fuente
2. Instala las dependencias Python
3. Ejecuta las pruebas con `pytest`
4. Inicia la aplicación y verifica que responde
5. Simula una fase de despliegue
6. Construye la imagen Docker `ghcr.io/andernarvaez05/ejercicio:3.0.0`
7. Se autentica en GitHub Container Registry
8. Publica la imagen

---

## Estructura del proyecto

```
Tarea3.0/
├── app.py                          # Aplicación Flask principal
├── test_app.py                     # Pruebas automatizadas (pytest)
├── requirements.txt                # Dependencias Python
├── Dockerfile                      # Imagen Docker
├── README.md                       # Este archivo
└── .github/
    └── workflows/
        └── python-application.yml  # Workflow CI/CD
```

---

**Tarea 3.0** · 5-VE-B-SD4-515-2026-I · Anderson Narváez
