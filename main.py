from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import hstack
import os

app = FastAPI()

# Definir variables globales pero no cargar datos ni modelos en el inicio
data = None
feature_matrix = None
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=200)

# Cargar dataset básico para endpoints que no son de recomendación
columnas_necesarias = ['title', 'release_date', 'vote_average', 'vote_count', 'cast_name', 'crew_name', 'return']
data_basico = pd.read_parquet(os.path.join("Movies", "dataclean.parquet"), columns=columnas_necesarias)

# Endpoint de bienvenida
@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de películas"}

# 1. Cantidad de filmaciones por mes
@app.get('/cantidad_filmaciones_mes/')
def cantidad_filmaciones_mes(mes: str):
    meses = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04', 
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08', 
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }
    mes_numero = meses.get(mes.lower())
    if not mes_numero:
        return {"error": "Mes inválido"}
    cantidad = data_basico[data_basico['release_date'].str[5:7] == mes_numero].shape[0]
    return {"mensaje": f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"}

# 2. Cantidad de filmaciones por día
@app.get('/cantidad_filmaciones_dia/')
def cantidad_filmaciones_dia(dia: str):
    dias = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'domingo': 6
    }
    dia_numero = dias.get(dia.lower())
    if dia_numero is None:
        return {"error": "Día inválido"}
    cantidad = data_basico[pd.to_datetime(data_basico['release_date']).dt.dayofweek == dia_numero].shape[0]
    return {"mensaje": f"{cantidad} cantidad de películas fueron estrenadas en el día {dia}"}

# 3. Puntaje de una película por título
@app.get('/score_titulo/')
def score_titulo(titulo: str):
    pelicula = data_basico[data_basico['title'].str.lower() == titulo.lower()]
    if pelicula.empty:
        return {"error": "Película no encontrada"}
    score = pelicula['vote_average'].values[0]
    return {"mensaje": f"La película '{titulo}' tiene un puntaje de {score}"}

# 4. Votos de una película por título
@app.get('/votos_titulo/')
def votos_titulo(titulo: str):
    pelicula = data_basico[data_basico['title'].str.lower() == titulo.lower()]
    if pelicula.empty:
        return {"error": "Película no encontrada"}
    votos = pelicula['vote_count'].values[0]
    return {"mensaje": f"La película '{titulo}' tiene un total de {votos} votos"}

# 5. Información de un actor
@app.get('/actor/{nombre_actor}')
def actor_info(nombre_actor: str):
    actor_data = data_basico[data_basico['cast_name'].str.contains(nombre_actor, case=False, na=False)]
    if actor_data.empty:
        return {"error": "Actor no encontrado"}
    total_peliculas = actor_data.shape[0]
    retorno_total = actor_data['return'].sum()
    return {
        "mensaje": f"El actor {nombre_actor} ha participado en {total_peliculas} películas y el retorno total es {retorno_total}"
    }

# 6. Información de un director
@app.get('/director/{nombre_director}')
def director_info(nombre_director: str):
    director_data = data_basico[data_basico['crew_name'].str.contains(nombre_director, case=False, na=False)]
    if director_data.empty:
        return {"error": "Director no encontrado"}
    cantidad_peliculas = director_data.shape[0]
    retorno_total = director_data['return'].sum()
    return {
        "mensaje": f"El director {nombre_director} ha dirigido {cantidad_peliculas} películas y el retorno total es {retorno_total}"
    }

# Función para cargar y procesar datos de recomendación bajo demanda
def cargar_datos_recomendacion():
    global data, feature_matrix
    if data is None:
        # Cargar solo una muestra del dataset
        columnas_recomendacion = ['title', 'overview', 'popularity', 'vote_average', 'genres_name', 'release_year']
        data = pd.read_parquet(os.path.join("Movies", "dataclean.parquet"), columns=columnas_recomendacion).head(1000)

        # Crear matriz TF-IDF
        tfidf_matrix = tfidf_vectorizer.fit_transform(data['overview'].fillna(''))

        # Vectorización de géneros y normalización de características
        genres_dummies = data['genres_name'].str.get_dummies(sep=',')
        data = pd.concat([data, genres_dummies], axis=1)
        scaler = MinMaxScaler()
        data[['popularity', 'vote_average', 'release_year']] = scaler.fit_transform(data[['popularity', 'vote_average', 'release_year']])

        # Crear la matriz de características
        numeric_features = data[['popularity', 'vote_average', 'release_year']].values
        feature_matrix = hstack([tfidf_matrix, genres_dummies.values, numeric_features]).tocsr()

# Función de recomendación
def get_recommendations(title):
    try:
        idx = data[data['title'].str.lower() == title.lower()].index[0]
        sim_scores = cosine_similarity(feature_matrix[idx], feature_matrix)[0]
        sim_scores = list(enumerate(sim_scores))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_indices = [i[0] for i in sim_scores[1:6]]
        return data['title'].iloc[sim_indices].tolist()
    except IndexError:
        return ["Película no encontrada"]

# Endpoint de recomendación
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    cargar_datos_recomendacion()  # Cargar datos y modelo bajo demanda
    recommendations = get_recommendations(titulo)
    return {"recommendations": recommendations}
