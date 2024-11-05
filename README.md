# Proyecto de Sistema de Recomendación de Películas

Este proyecto es una API desarrollada con FastAPI que proporciona recomendaciones de películas basadas en similitudes y permite consultar información sobre películas, actores y directores.

## Descripción
La API permite realizar varias consultas, como la cantidad de filmaciones por mes o día, obtener recomendaciones de películas basadas en el título, y consultar información detallada de actores y directores. Además, se incluyen archivos de datos preprocesados para el análisis y procesamiento.

## Estructura del Proyecto

- **Movies/**: Contiene los datasets utilizados en el proyecto.
  - `credits.csv`: Dataset con información sobre los créditos de las películas.
  - `creditsfinal.csv`: Versión final del dataset de créditos tras el procesamiento.
  - `dataclean.csv`: Dataset principal de películas después de la limpieza inicial.
  - `dataclean.parquet`: Versión en formato Parquet del dataset `dataclean.csv` para optimizar la carga de datos.
  - `df_final_exported.csv`: Dataset combinado final después del procesamiento.
  - `movies_dataset.csv`: Dataset original de películas.

- **venv/**: Carpeta que contiene el entorno virtual, donde están instaladas las dependencias del proyecto.

- **main.py**: Archivo principal que contiene el código de la API, incluyendo todos los endpoints.

- **creditsdesanidado.ipynb** y **unircreditsymovies.ipynb**: Notebooks que documentan el proceso de preprocesamiento de datos, como la desanidación de columnas y la combinación de datasets.

- **requirements.txt**: Archivo que especifica las dependencias necesarias para ejecutar la API.

- **README.md**: Este archivo de documentación que describe el proyecto y su estructura.

## Requisitos Previos
- Python 3.8 o superior
- FastAPI
- scikit-learn
- pandas
- numpy
- pyarrow

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
Navega al directorio del proyecto:
bash
Copiar código
cd tu_repositorio
Instala las dependencias:
bash
Copiar código
pip install -r requirements.txt

Ejecución de la API

Para iniciar la API, usa el siguiente comando:

bash
Copiar código
uvicorn main:app --reload
La API estará disponible en http://127.0.0.1:8000.

## Endpoints de la API

/cantidad_filmaciones_mes/{mes}: Devuelve el número de películas lanzadas en un mes específico.
/cantidad_filmaciones_dia/{dia}: Devuelve el número de películas lanzadas en un día específico.
/score_titulo/{titulo}: Devuelve el puntaje promedio de una película por título.
/votos_titulo/{titulo}: Devuelve el número de votos de una película específica.
/actor/{nombre_actor}: Muestra la cantidad de películas y el retorno total para un actor.
/director/{nombre_director}: Muestra la cantidad de películas y el retorno total para un director.
/recomendacion/{titulo}: Devuelve una lista de 5 películas recomendadas basadas en el título ingresado.

Notas
Este proyecto fue creado como parte de un ejercicio de aprendizaje para desarrollar sistemas de recomendación y APIs usando FastAPI. Los notebooks .ipynb documentan el proceso de preprocesamiento de datos, que es fundamental para la creación de un sistema de recomendación efectivo.