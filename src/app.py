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

st.markdown(
    """
    <style>

    /* Fondo general */
    .stApp {
        background: linear-gradient(
            180deg,
            #1e3a8a 0%,
            #020617 100%
        );
    }

    /* Card libro */
    .libro-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);

        backdrop-filter: blur(10px);

        border-radius: 24px;

        padding: 25px;

        margin-bottom: 30px;

        transition: all 0.3s ease;

        box-shadow:
        0px 4px 20px rgba(0,0,0,0.25);
    }

    .libro-card:hover {

        transform: translateY(-5px);

        border: 1px solid rgba(255,255,255,0.15);

        box-shadow:
        0px 10px 30px rgba(0,0,0,0.4);
    }

    /* Hover portada */
[data-testid="stImage"] img {

    border-radius: 16px;

    transition: all 0.3s ease;

    cursor: pointer;
}

[data-testid="stImage"] img:hover {

    transform: scale(1.06);

    box-shadow:
    0px 0px 30px rgba(255,255,255,0.18);
}

/* Fondo general */

/* INPUT */
div[data-baseweb="input"] {

    background: rgba(30,58,138,0.45) !important;

    border-radius: 16px !important;

    border: 1px solid rgba(255,255,255,0.12) !important;

    transition: all 0.3s ease !important;
}

div[data-baseweb="input"]:focus-within {

    border: 1px solid #60a5fa !important;

    box-shadow:
    0px 0px 20px rgba(96,165,250,0.35) !important;
}

/* INPUT INTERNO */
div[data-baseweb="input"] input {

    background: transparent !important;

    color: white !important;

    font-size: 16px !important;
}

/* BOTONES */
.stButton > button {

    background: rgba(30,58,138,0.55) !important;

    color: white !important;

    border-radius: 16px !important;

    border: 1px solid rgba(255,255,255,0.12) !important;

    padding: 10px 22px !important;

    font-weight: 600 !important;

    transition: all 0.3s ease !important;
}

/* HOVER BOTONES */
.stButton > button:hover {

    background: rgba(59,130,246,0.35) !important;

    border: 1px solid #60a5fa !important;

    transform: translateY(-2px);

    box-shadow:
    0px 0px 20px rgba(96,165,250,0.25) !important;
}
    </style>
    """,
    unsafe_allow_html=True
)

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

    for i, (_, libro) in enumerate(
        st.session_state.resultados.iterrows(),
        start=1
    ):

        
        col_num, col1, col2 = st.columns([0.4, 1, 3])

        # =====================================
        # IMAGEN
        # =====================================

        with col_num:

            st.markdown(
                f"""
                <div style="
                    font-size: 80px;
                    font-weight: bold;
                    color: #C0C0C0;
                    text-align: left;
                    padding-left: 10px;
                    margin-top: 40px;
                    opacity: 0.8;
                    text-shadow: 0px 0px 10px rgba(255,255,255,0.2);
                    -webkit-text-stroke: 2px rgba(255,255,255,0.1);
                ">
                    {i}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col1:

            if (
                "thumbnail" in libro
                and libro["thumbnail"]
                and str(libro["thumbnail"]) != "nan"
            ):

                try:

                    st.markdown(
                        '<div class="portada-hover">',
                        unsafe_allow_html=True
                    )
                    
                    st.image(
                        libro["thumbnail"],
                        width=150
                    )
                    
                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
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

           # with st.expander("📖 Descripción"):

            #    descripcion_es = Traductor.traducir(
             #       libro["description"],
              #      destino = "es"
               # )

                #st.write(descripcion_es)


            with st.expander("📖 Ver descripción"):

                descripcion_es = Traductor.traducir(
                    libro["description"],
                    destino="es"
                )

               
        


            st.divider()
            st.divider()

            
