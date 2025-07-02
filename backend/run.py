import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",   # app = FastAPI() dentro de app/main.py
        host="localhost",   # Escucha en todas las interfaces (útil para acceder desde tu celular)
        port=8000,        # Cambia si deseas otro puerto
        reload=True       # Auto recarga si cambias archivos (solo en desarrollo)
    )