from app.core.database import Base, engine
from Backend.app.models.user import User  # Importa el modelo
from app.models.embedding import Embedding  # Importa el modelo

def init_db():
    print("🧱 Creando las tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ ¡Tablas creadas exitosamente!")

if __name__ == "__main__":
    init_db()