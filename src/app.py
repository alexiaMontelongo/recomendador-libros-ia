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

# Inicializar estado
if "busqueda" not in st.session_state:

    st.session_state.busqueda = ""

# Función limpiar
def limpiar_busqueda():

    st.session_state.busqueda = ""

# Layout
col1, col2 = st.columns([8, 1])

with col1:

    consulta = st.text_input(
        "¿Qué libro buscas?",
        key="busqueda"
    )

with col2:

    st.write("")

    st.button(
        "❌",
        on_click=limpiar_busqueda
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

                if (
                        "thumbnail" in libro
                        and libro["thumbnail"]
                        and str(libro["thumbnail"]) != "nan"
                    ):

                        try:

                            st.image(
                                libro["thumbnail"],
                                width=150
                            )

                        except:

                            st.write("Imagen no disponible")

                else:
                    
                    st.markdown(
                    """
                    <div style="
                        height: 220px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        border: 1px solid gray;
                        border-radius: 10px;
                    ">
                        Imagen no disponible
                    </div>
                    """,
                    unsafe_allow_html=True
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