
import pandas as pd
import re

from modelo_ia import ModeloIA
from traduccion import Traductor


class RecomendadorLibros:

    def __init__(self):

        print("Cargando dataset...")

        # Leer dataset
        self.df = pd.read_csv("data/libros.csv")

        # Rellenar vacíos
        self.df = self.df.fillna("")

        # Convertir páginas
        self.df["num_pages"] = pd.to_numeric(
            self.df["num_pages"],
            errors="coerce"
        )

        self.df["num_pages"] = (
            self.df["num_pages"].fillna(0)
        )


        # Convertir rating
        self.df["average_rating"] = pd.to_numeric(
            self.df["average_rating"],
            errors="coerce"
        ).fillna(0)

        # Convertir cantidad de ratings
        self.df["ratings_count"] = pd.to_numeric(
            self.df["ratings_count"],
            errors="coerce"
        ).fillna(0)

        print("Preparando información de libros...")

        # Combinar texto
        self.textos_libros = (
            self.df["title"].astype(str) + " " +
            self.df["categories"].astype(str) + " " +
            self.df["description"].astype(str)
        )

        # Crear IA
        self.modelo_ia = ModeloIA(
            self.textos_libros.tolist()
        )

        print("Sistema listo.\n")

    def recomendar(self, consulta_usuario):

        # Traducir consulta
        consulta_ingles = Traductor.traducir(
            consulta_usuario
        )

        print(
            f"\nConsulta traducida: "
            f"{consulta_ingles}"
        )

        # Buscar similares
        similitudes = (
            self.modelo_ia.buscar_similares(
                consulta_ingles
            )
        )

        # Copia temporal
        resultados_df = self.df.copy()

        resultados_df["similitud"] = similitudes

        # ==========================================
        # NORMALIZAR RATING
        # ==========================================

        resultados_df["rating_normalizado"] = (
            resultados_df["average_rating"] / 5
        )

        # ==========================================
        # NORMALIZAR POPULARIDAD
        # ==========================================

        max_reviews = resultados_df["ratings_count"].max()

        resultados_df["popularidad_normalizada"] = (
            resultados_df["ratings_count"] / max_reviews
        )

        # ==========================================
        # SCORE FINAL
        # ==========================================

        resultados_df["score_final"] = (
            resultados_df["similitud"] * 0.75
            +
            resultados_df["rating_normalizado"] * 0.15
            +
            resultados_df["popularidad_normalizada"] * 0.10
        )


        # ==========================================
        # FILTRO CALIDAD
        # ==========================================

        resultados_df = resultados_df[
            (
                resultados_df["average_rating"] >= 4.0
            )
            &
            (
                resultados_df["ratings_count"] >= 1000
            )
        ]

        consulta_lower = consulta_usuario.lower()

        # ==========================================
        # LIBRO CORTO O LARGO
        # ==========================================

        if "corto" in consulta_lower:

            resultados_df = resultados_df[
                resultados_df["num_pages"] < 300
            ]

        elif "largo" in consulta_lower:

            resultados_df = resultados_df[
                resultados_df["num_pages"] > 500
            ]

        # ==========================================
        # DETECTAR PÁGINAS
        # ==========================================

        numeros = re.findall(
            r'\d+',
            consulta_lower
        )

        if numeros:

            paginas_deseadas = int(numeros[0])

            print(
                f"Páginas detectadas: "
                f"{paginas_deseadas}"
            )

            margen = 50

            resultados_df = resultados_df[
                (
                    resultados_df["num_pages"]
                    >= paginas_deseadas - margen
                )
                &
                (
                    resultados_df["num_pages"]
                    <= paginas_deseadas + margen
                )
            ]

        # ==========================================
        # ORDENAR RESULTADOS
        # ==========================================

        top_libros = resultados_df.sort_values(
            by="score_final",
            ascending=False
        ).head(5)

        return top_libros[
            [
                "title",
                "authors",
                "categories",
                "num_pages",
                "average_rating",
                "thumbnail"
                #"score_final"
            ]
        ]
    



    