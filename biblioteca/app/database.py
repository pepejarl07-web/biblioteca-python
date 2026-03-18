import os
from pymongo import MongoClient
from dotenv import load_dotenv

# cargar variables d entorno
load_dotenv()

#obtener la uri de mongodb
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("No se ha encontrado mongo en las variables de entorno")

#conectar mongodb
client = MongoClient(MONGO_URI)

#seleccioanr base de datos
db = client["coco"]

books_collection = db["books"]
users_collection = db["users"]

print("Conexion a mongo establecida OK")

#prueba xa listar las bases de datos

print("Bases de datos disponibles:", client.list_database_names())