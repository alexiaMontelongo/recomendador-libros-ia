import os
import joblib

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class ModeloIA:

    def __init__(self, textos_libros):

        print("Cargando modelo de IA...")

        self.modelo = SentenceTransformer(
            'all-MiniLM-L6-v2'
        )

        ruta_embeddings = "models/embeddings.pkl"

        # Verificar embeddings
        if os.path.exists(ruta_embeddings):

            print("Cargando embeddings guardados...")

            self.embeddings = joblib.load(
                ruta_embeddings
            )

        else:

            print("Creando embeddings por primera vez...")

            self.embeddings = self.modelo.encode(
                textos_libros,
                show_progress_bar=True
            )

            joblib.dump(
                self.embeddings,
                ruta_embeddings
            )

            print("Embeddings guardados.")

    def buscar_similares(self, consulta):

        # Embedding consulta
        embedding_consulta = self.modelo.encode(
            [consulta]
        )

        # Similaridad coseno
        similitudes = cosine_similarity(
            embedding_consulta,
            self.embeddings
        )[0]

        return similitudes
    