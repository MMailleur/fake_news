# 1. Library imports
import uvicorn
from typing import List
from models import Test
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import pymysql
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
#conneries

# Récupérer l'URL de la base de données à partir des variables d'environnement
database_url = os.getenv("DATABASE_URL")

# Extraire les composants de l'URL de la base de données
url_components = urlparse(database_url)
db_host = url_components.hostname
db_user = url_components.username
db_password = url_components.password
db_name = url_components.path.strip('/')

# Configurer la connexion à la base de données MySQL
conn = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)


#----------------- Définir les routes de l'API-----------------------------#

@app.get("/")
async def get_hello():
    return {"hello":"world"}

@app.get("/data")
async def get_items():
    # Effectuer des opérations sur la base de données
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM test")
        results = cursor.fetchall()
    # Retourner les résultats de l'API
    return {"items": results}

# # 4. Run the API with uvicorn
# #    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
