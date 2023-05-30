# 1. Library imports
import uvicorn
from typing import List
from models import Model_out,Model_pred
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import pymysql
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import pickle



def load_model():
    vec = pickle.load(open("vectext.pickle", "rb"))
    model = pickle.load(open("model1.pickle", 'rb'))
    return model,vec
model ,vec = load_model()


load_dotenv()
app = FastAPI()

#conneries
def connect():
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
    return conn


#----------------- Définir les routes de l'API-----------------------------#

@app.get("/")
async def get_hello():
    return {"hello":"world"}

@app.get("/datasample")
async def get_items():
    # Effectuer des opérations sur la base de données
    conn = connect()

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM train_data LIMIT 2")
        results = cursor.fetchall()
    # Retourner les résultats de l'API

    conn.close()
    return {"items": results}

@app.get("/data")
async def get_items(label :int =0 ,nbrow : int =5 ,lengthtext : int =200):
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute(f" (SELECT * FROM fakebase.train_data \
where LENGTH(text) > {lengthtext} and title >10 and label = {label}  \
ORDER BY LENGTH(text) asc LIMIT {nbrow})")

        results = cursor.fetchall()
    # Retourner les résultats de l'API
    conn.close()
    return {"items": results}

@app.get("/datastem")
async def get_items(label :int =0 ,nbrow : int =5 ,lengthtext : int =200):
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute(f" (SELECT * FROM fakebase.stem_data \
where LENGTH(text) > {lengthtext} and title >10  \
ORDER BY LENGTH(text) asc LIMIT {nbrow})")
        results = cursor.fetchall()
    # Retourner les résultats de l'API
    conn.close()
    return {"items": results}


@app.get("/dataoutput")
async def get_items():
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute(f" (SELECT * FROM fakebase.output_data LIMIT 5 )")
        results = cursor.fetchall()
    # Retourner les résultats de l'API
    conn.close()
    return {"items": results}

@app.post("/add")
async def create_item(item: Model_out):
    # Perform operations on the database
    conn = connect()
    with conn.cursor() as cursor:
        query = "INSERT INTO output_data (id,title,author,text,label) " \
                 "VALUES (%s, %s, %s, %s, %s)"
        values = (item.id, item.title, item.author, item.text, item.label)
        cursor.execute(query, values)
        conn.commit()
    conn.close()
    return {"message": "Item created successfully"}

@app.post("/addpred")
async def create_item(item: Model_pred):
    # Perform operations on the database
    conn = connect()
    with conn.cursor() as cursor:
        query = "INSERT INTO output_data (id,title,author,text,pred) " \
                 "VALUES (%s, %s, %s, %s, %s)"
        values = (item.id, item.title, item.author, item.text, item.pred)
        cursor.execute(query, values)
        conn.commit()
    conn.close()
    return {"message": "Item created successfully"}

@app.get('/predict')
def predict(stem_text: str = ""):
    stem_obj = [stem_text]
    stem_vec = vec.transform(stem_obj)
    prediction  = model.predict(stem_vec)

    return {str(prediction[0])}


# # 4. Run the API with uvicorn
# #    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
