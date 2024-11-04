from fastapi import FastAPI
import pandas as pd

# Carga el dataset
data = pd.read_parquet(r"Movies\dataclean.parquet")

app = FastAPI()


@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de películas"}

# 1. Cantidad de filmaciones por mes
@app.get('/cantidad_filmaciones_mes/')
def cantidad_filmaciones_mes(mes: str):
    meses = {'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04', 'mayo': '05', 'junio': '06',
             'julio': '07', 'agosto': '08', 'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'}
    mes_numero = meses.get(mes.lower())
    if not mes_numero:
        return {"error": "Mes inválido"}
    cantidad = data[data['release_date'].str[5:7] == mes_numero].shape[0]
    return {"mensaje": f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"}

# 2. Cantidad de filmaciones por día
@app.get('/cantidad_filmaciones_dia/')
def cantidad_filmaciones_dia(dia: str):
    dias = {'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'domingo': 6}
    dia_numero = dias.get(dia.lower())
    if dia_numero is None:
        return {"error": "Día inválido"}
    data['release_day'] = pd.to_datetime(data['release_date'], errors='coerce').dt.dayofweek
    cantidad = data[data['release_day'] == dia_numero].shape[0]
    return {"mensaje": f"{cantidad} cantidad de películas fueron estrenadas en los días {dia}"}

# 3. Score por título
@app.get('/score_titulo/')
def score_titulo(titulo: str):
    film = data[data['title'].str.lower() == titulo.lower()]
    if film.empty:
        return {"error": "Película no encontrada"}
    año = film['release_year'].values[0]
    score = film['popularity'].values[0]
    return {"mensaje": f"La película {titulo} fue estrenada en el año {año} con un score de {score}"}

# 4. Votos por título
@app.get('/votos_titulo/')
def votos_titulo(titulo: str):
    film = data[data['title'].str.lower() == titulo.lower()]
    if film.empty:
        return {"error": "Película no encontrada"}
    votos = film['vote_count'].values[0]
    promedio_votos = film['vote_average'].values[0]
    if votos < 2000:
        return {"mensaje": "La película no cumple con la condición de tener al menos 2000 valoraciones"}
    return {"mensaje": f"La película {titulo} cuenta con {votos} valoraciones, con un promedio de {promedio_votos}"}

# 5. Información sobre el actor
@app.get('/get_actor/')
def get_actor(nombre_actor: str):
    actor_films = data[data['cast_name'].str.contains(nombre_actor, case=False, na=False)]
    if actor_films.empty:
        return {"error": "Actor no encontrado"}
    retorno_total = actor_films['return'].sum()
    cantidad_peliculas = actor_films.shape[0]
    promedio_retorno = retorno_total / cantidad_peliculas
    return {"mensaje": f"El actor {nombre_actor} ha participado en {cantidad_peliculas} películas, "
                       f"con un retorno total de {retorno_total} y un promedio de {promedio_retorno} por película"}

# 6. Información sobre el director
@app.get('/get_director/')
def get_director(nombre_director: str):
    director_films = data[data['crew_name'].str.contains(nombre_director, case=False, na=False) & (data['crew_job'] == 'Director')]
    if director_films.empty:
        return {"error": "Director no encontrado"}
    peliculas = []
    for _, row in director_films.iterrows():
        peliculas.append({
            "titulo": row['title'],
            "fecha_lanzamiento": row['release_date'],
            "retorno_individual": row['return'],
            "costo": row['budget'],
            "ganancia": row['revenue'] - row['budget']
        })
    return {"director": nombre_director, "peliculas": peliculas}


#activar el entorno
# .\venv\Scripts\activate

#instalar 
#uvicorn main:app --reload

#Para ver la documentación interactiva de Swagger UI que te permite interactuar con los endpoints, ve a:

#Swagger UI: http://127.0.0.1:8000/docs
#Redoc: http://127.0.0.1:8000/redoc