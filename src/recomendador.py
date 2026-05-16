import os
import joblib
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from deep_translator import GoogleTranslator


class RecomendadorLibros:

    def __init__(self):

        print("Cargando dataset...")

        # Leer dataset
        self.df = pd.read_csv("data/libros.csv")

        # Rellenar vacíos
        self.df = self.df.fillna("")

        print("Cargando modelo de IA...")

        # Modelo NLP
        self.modelo = SentenceTransformer('all-MiniLM-L6-v2')

        # Ruta embeddings
        ruta_embeddings = "models/embeddings.pkl"

        print("Preparando información de libros...")

        # Combinar texto SIN modificar CSV
        self.textos_libros = (
            self.df["title"].astype(str) + " " +
            self.df["categories"].astype(str) + " " +
            self.df["description"].astype(str)
        )

        # Verificar si ya existen embeddings
        if os.path.exists(ruta_embeddings):

            print("Cargando embeddings guardados...")

            self.embeddings = joblib.load(ruta_embeddings)

        else:

            print("Creando embeddings por primera vez...")

            self.embeddings = self.modelo.encode(
                self.textos_libros.tolist(),
                show_progress_bar=True
            )

            # Guardar embeddings
            joblib.dump(
                self.embeddings,
                ruta_embeddings
            )

            print("Embeddings guardados.")

        print("Sistema listo.\n")


    def traducir_texto(self, texto):

        traduccion = GoogleTranslator(
            source='auto',
            target='en'
        ).translate(texto)

        return traduccion


    def recomendar(self, consulta_usuario):

        # Traducir consulta
        consulta_ingles = self.traducir_texto(consulta_usuario)

        print(f"\nConsulta traducida: {consulta_ingles}")

        # Embedding consulta
        embedding_consulta = self.modelo.encode([consulta_ingles])

        # Similaridades
        similitudes = cosine_similarity(
            embedding_consulta,
            self.embeddings
        )[0]

        # Copia temporal
        resultados_df = self.df.copy()

        # Agregar similitud
        resultados_df["similitud"] = similitudes

        consulta_lower = consulta_usuario.lower()

        # Detectar longitud
        if "corto" in consulta_lower:

            resultados_df = resultados_df[
                resultados_df["num_pages"] < 300
            ]

        elif "largo" in consulta_lower:

            resultados_df = resultados_df[
                resultados_df["num_pages"] > 500
            ]

        # Ordenar resultados
        top_libros = resultados_df.sort_values(
            by="similitud",
            ascending=False
        ).head(5)

        return top_libros[
            [
                "title",
                "authors",
                "categories",
                "num_pages",
                "average_rating"
            ]
        ]