import streamlit as st

from traduccion import Traductor

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
# ESTADOS
# =====================================

if "busqueda" not in st.session_state:

    st.session_state.busqueda = ""

if "resultados" not in st.session_state:

    st.session_state.resultados = None

# =====================================
# FUNCIÓN LIMPIAR
# =====================================

def limpiar_busqueda():

    del st.session_state["busqueda"]

    st.rerun()

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
# FORMULARIO BÚSQUEDA
# =====================================

col1, col2 = st.columns([8, 1])

with col1:

    with st.form("form_busqueda"):

        consulta = st.text_input(
            "¿Qué libro buscas?",
            key="busqueda"
        )

        buscar = st.form_submit_button(
            "Buscar"
        )

with col2:

    st.write("")

    st.write("")

    if st.button("❌"):

        limpiar_busqueda()

# =====================================
# EJECUTAR BÚSQUEDA
# =====================================

if buscar:

    if consulta.strip() != "":

        with st.spinner(
            "Buscando libros..."
        ):

            st.session_state.resultados = (
                recomendador.recomendar(
                    consulta
                )
            )

# =====================================
# MOSTRAR RESULTADOS
# =====================================

if st.session_state.resultados is not None:

    st.subheader("Resultados")

    for _, libro in (
        st.session_state.resultados.iterrows()
    ):

        col1, col2 = st.columns([1, 3])

        # =====================================
        # IMAGEN
        # =====================================

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

        # =====================================
        # INFORMACIÓN LIBRO
        # =====================================

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

            # =====================================
            # NIVEL DE CONFIANZA
            # =====================================

            confianza = libro["score_final"] * 100
            confianza = min(
                80 + (libro["score_final"] * 20),
                99
            )


            # st.write(
             #   f"🤖 Nivel de confianza: "
             #   f"{confianza:.2f}%"
            #) 

            #st.progress(float(libro["score_final"]))


           # =====================================
            # DESCRIPCIÓN DESPLEGABLE
            # =====================================

            with st.expander("📖 Descripción"):

                descripcion_es = Traductor.traducir(
                    libro["description"]
                )

                st.write(descripcion_es)


            st.divider()