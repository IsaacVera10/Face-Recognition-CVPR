# CVPR-Final_Project
| Carpeta / Archivo        | Rol                                                                           |
| ------------------------ | ----------------------------------------------------------------------------- |
| `main.py`                | Inicializa la app, monta las rutas, configura CORS, etc.                      |
| `api/recognize.py`       | Contiene el endpoint `/recognize` que recibe imágenes y responde              |
| `core/config.py`         | Configuración general: puertos, paths, debug, CORS, etc.                      |
| `models/response.py`     | Define cómo se estructura la respuesta del backend (bounding boxes + nombres) |
| `services/detector.py`   | Carga y ejecuta el modelo de detección de rostros                             |
| `services/recognizer.py` | Gestiona embeddings y compara para identificar personas                       |
| `services/utils.py`      | Decodifica imágenes, convierte formatos, etc.                                 |
| `data/face_db.npy`       | Base de datos de embeddings (puedes usar un archivo .npy o SQLite)            |
## 📦 Instalación (usando Conda)

```bash
# Clonar el repositorio
git clone <url-del-repo>
cd backend

# Crear un nuevo entorno Conda (recomendado)
conda create --name fastapi-env --file conda_requirements.txt
conda activate fastapi-env
```
## 🚀 Ejecutar la API

```bash
# Desde la raíz del backend
python run.py
```

* El servidor iniciará en: http://localhost:8000
* Swagger Docs (documentación interactiva): http://localhost:8000/docs
* Endpoint de reconocimiento facial: POST /recognize

