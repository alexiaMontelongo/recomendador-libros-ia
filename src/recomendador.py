import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from deep_translator import GoogleTranslator


class RecomendadorLibros:

    def __init__(self):

        print("Cargando dataset...")

        # Leer dataset
        self.df = pd.read_csv("data/libros.csv")

        # Rellenar valores vacíos
        self.df = self.df.fillna("")

        print("Cargando modelo de IA...")

        # Modelo NLP
        self.modelo = SentenceTransformer('all-MiniLM-L6-v2')

        print("Preparando información de libros...")

        # Combinar información SIN modificar el CSV
        self.textos_libros = (
            self.df["title"].astype(str) + " " +
            self.df["categories"].astype(str) + " " +
            self.df["description"].astype(str)
        )

        # Crear embeddings
        self.embeddings = self.modelo.encode(
            self.textos_libros.tolist(),
            show_progress_bar=True
        )

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

        # Embedding de consulta
        embedding_consulta = self.modelo.encode([consulta_ingles])

        # Similaridad
        similitudes = cosine_similarity(
            embedding_consulta,
            self.embeddings
        )[0]

        # Agregar similitud al dataframe temporalmente
        self.df["similitud"] = similitudes

        # Detectar preferencias de longitud
        consulta_lower = consulta_usuario.lower()

        if "corto" in consulta_lower:
            resultados = self.df[self.df["num_pages"] < 300]

        elif "largo" in consulta_lower:
            resultados = self.df[self.df["num_pages"] > 500]

        else:
            resultados = self.df

        # Top 5 mejores
        top_libros = resultados.sort_values(
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