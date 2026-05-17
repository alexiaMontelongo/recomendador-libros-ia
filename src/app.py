import streamlit as st

from recomendador import (
    RecomendadorLibros
)

# =====================================
# CONFIGURACIÓN PÁGINA
# =====================================

st.set_page_config(
    page_title="Recomendador de Libros IA",
    page_icon="📚",
    layout="wide"
)

# =====================================
# TÍTULO
# =====================================

st.title("📚 Recomendador de Libros con IA")

st.write(
    "Busca libros usando inteligencia artificial."
)

# =====================================
# CARGAR SISTEMA
# =====================================

@st.cache_resource
def cargar_recomendador():

    return RecomendadorLibros()

recomendador = cargar_recomendador()

# =====================================
# INPUT USUARIO
# =====================================

consulta = st.text_input(
    "¿Qué libro buscas?"
)

# =====================================
# BOTÓN
# =====================================

if st.button("Buscar"):

    if consulta.strip() != "":

        with st.spinner(
            "Buscando libros..."
        ):

            resultados = recomendador.recomendar(
                consulta
            )

        st.subheader("Resultados")

        for _, libro in resultados.iterrows():

            col1, col2 = st.columns([1, 3])

            with col1:

                # Imagen libro
                if "thumbnail" in libro:

                    st.image(
                        libro["thumbnail"],
                        width=150
                    )

            with col2:

                st.markdown(
                    f"## {libro['title']}"
                )

                st.write(
                    f"✍️ Autor: "
                    f"{libro['authors']}"
                )

                st.write(
                    f"📚 Categoría: "
                    f"{libro['categories']}"
                )

                st.write(
                    f"📖 Páginas: "
                    f"{libro['num_pages']}"
                )

                st.write(
                    f"⭐ Rating: "
                    f"{libro['average_rating']}"
                )

                st.divider()