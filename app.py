import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Museo del Louvre",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Poppins:wght@300;400;500;600&display=swap');

/* =====================================================
   FONDO GENERAL
===================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 8% 10%,
            rgba(173, 112, 55, 0.28) 0%,
            rgba(100, 55, 25, 0.15) 25%,
            transparent 48%
        ),
        radial-gradient(
            circle at 90% 85%,
            rgba(120, 70, 35, 0.30) 0%,
            rgba(75, 38, 20, 0.16) 28%,
            transparent 55%
        ),
        linear-gradient(
            125deg,
            #090604 0%,
            #1c0f08 20%,
            #3a1e10 42%,
            #512a14 58%,
            #261309 78%,
            #070403 100%
        );

    background-attachment: fixed;
}

/* =====================================================
   ELEMENTOS DE STREAMLIT
   IMPORTANTE:
   NO OCULTAMOS EL HEADER NI EL TOOLBAR
   PARA CONSERVAR EL BOTÓN DEL SIDEBAR
===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Dejamos visible el encabezado de Streamlit */
header {
    background: transparent !important;
}

/* =====================================================
   CONTENEDOR
===================================================== */

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* =====================================================
   TÍTULO PRINCIPAL
===================================================== */

.museum-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 48px;
    font-weight: 600;
    letter-spacing: 7px;
    color: #ffffff;
    text-align: center;
    margin-bottom: 5px;
}

.museum-subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: 13px;
    font-weight: 400;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #d9a441;
    text-align: center;
    margin-bottom: 25px;
}

.gold-line {
    width: 90px;
    height: 2px;
    background: #d9a441;
    margin: 0 auto 45px auto;
}

/* =====================================================
   TÍTULOS DE LA OBRA
===================================================== */

.art-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 42px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 3px;
}

.art-subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: 13px;
    color: #d9a441;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 18px;
}

.art-description {
    font-family: 'Poppins', sans-serif;
    font-size: 15px;
    line-height: 1.9;
    font-weight: 300;
    color: #ffffff;
    text-align: justify;
}

/* =====================================================
   IMAGEN
===================================================== */

.image-frame {
    border: 1px solid rgba(217, 164, 65, 0.75);
    padding: 8px;
    background: rgba(0, 0, 0, 0.25);
    box-shadow: 0 12px 35px rgba(0,0,0,0.45);
}

/* =====================================================
   SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #120a06 0%,
            #251209 50%,
            #100704 100%
        );

    border-right: 1px solid rgba(217,164,65,0.35);
}

section[data-testid="stSidebar"] h2 {
    font-family: 'Cormorant Garamond', serif;
    color: #d9a441;
    font-size: 27px;
}

section[data-testid="stSidebar"] p {
    font-family: 'Poppins', sans-serif;
    color: #ffffff !important;
    font-size: 14px;
    line-height: 1.7;
}

/* =====================================================
   TEXTOS Y ETIQUETAS
===================================================== */

label {
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff !important;
}

div[data-baseweb="select"] * {
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff !important;
}

/* =====================================================
   CAJA DE TEXTO
===================================================== */

textarea {
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff !important;
    background-color: rgba(0,0,0,0.35) !important;
    border: 1px solid rgba(217,164,65,0.45) !important;
}

textarea::placeholder {
    color: #ffffff !important;
    opacity: 0.75 !important;
}

/* =====================================================
   SELECTOR DE IDIOMA
===================================================== */

div[data-baseweb="select"] > div {
    background-color: rgba(0,0,0,0.35) !important;
    border: 1px solid rgba(217,164,65,0.45) !important;
}

/* =====================================================
   BOTÓN
===================================================== */

.stButton > button {
    width: 100%;

    background: linear-gradient(
        135deg,
        #d9a441,
        #b87b25
    );

    color: #1a0c05 !important;
    border: none;
    border-radius: 4px;

    padding: 12px 20px;

    font-family: 'Poppins', sans-serif;
    font-size: 14px;
    font-weight: 600;

    letter-spacing: 1px;

    transition: 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #edc36a,
        #d9a441
    );

    transform: translateY(-1px);
}

/* =====================================================
   AUDIO
===================================================== */

.audio-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 30px;
    color: #d9a441;
    margin-top: 30px;
    margin-bottom: 10px;
}

/* =====================================================
   SEPARADOR
===================================================== */

.separator {
    height: 1px;
    background: rgba(217,164,65,0.35);
    margin: 45px 0;
}

/* =====================================================
   PIE
===================================================== */

.footer {
    text-align: center;
    font-family: 'Poppins', sans-serif;
    font-size: 11px;
    color: #ffffff;
    opacity: 0.7;
    margin-top: 50px;
    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    '<div class="museum-title">MUSEO DEL LOUVRE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="museum-subtitle">Colección permanente · París</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="gold-line"></div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<h2>🎧 Audioguía</h2>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p>
        Escribe o selecciona un texto para escucharlo.
        Selecciona el idioma y convierte el texto en una
        audioguía.
        </p>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CARPETA TEMPORAL
# =========================================================

try:
    os.mkdir("temp")
except:
    pass


# =========================================================
# INFORMACIÓN DE LA MONA LISA
# =========================================================

col1, col2 = st.columns([0.95, 1.25], gap="large")


# =========================================================
# COLUMNA IZQUIERDA
# =========================================================

with col1:

    image = Image.open("monalisa.jpg")

    st.markdown(
        '<div class="image-frame">',
        unsafe_allow_html=True
    )

    st.image(
        image,
        width=350
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# COLUMNA DERECHA
# =========================================================

with col2:

    st.markdown(
        '<div class="art-title">La Mona Lisa</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="art-subtitle">Leonardo da Vinci · Siglo XVI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="art-description">

        La Gioconda o Mona Lisa es una célebre obra pictórica
        al óleo de Leonardo da Vinci, creada en su natal
        Florencia entre los años 1503 y 1506, posiblemente
        continuando hasta aproximadamente 1515 o 1517,
        aunque esta fecha de conclusión tan imprecisa es
        objeto de debate.

        <br><br>

        La teoría más aceptada indica que retrata a
        Lisa Gherardini, la esposa del rico comerciante
        de sedas Francesco del Giocondo, motivo por el cual
        lleva también el nombre de La Gioconda.

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SEPARADOR
# =========================================================

st.markdown(
    '<div class="separator"></div>',
    unsafe_allow_html=True
)


# =========================================================
# AUDIOGUÍA
# =========================================================

st.markdown(
    '<div class="audio-title">Escucha la obra</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        font-family:Poppins, sans-serif;
        color:white;
        font-size:14px;
    ">
    Copia o escribe el texto que deseas escuchar.
    </p>
    """,
    unsafe_allow_html=True
)


text = st.text_area(
    "Ingrese el texto a escuchar.",
    height=150,
    placeholder="Escribe aquí el texto de la audioguía..."
)


# =========================================================
# IDIOMA
# =========================================================

option_lang = st.selectbox(
    "Selecciona el idioma",
    ("Español", "English")
)

if option_lang == "Español":
    lg = "es"
else:
    lg = "en"


# =========================================================
# FUNCIÓN TEXT TO SPEECH
# =========================================================

def text_to_speech(text, tld, lg):

    tts = gTTS(
        text=text,
        lang=lg
    )

    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"

    # Evitar caracteres problemáticos en el nombre
    my_file_name = "".join(
        c for c in my_file_name
        if c.isalnum() or c in (" ", "_", "-")
    )

    if not my_file_name:
        my_file_name = "audio"

    file_path = f"temp/{my_file_name}.mp3"

    tts.save(file_path)

    return my_file_name, text


# =========================================================
# BOTÓN CONVERTIR
# =========================================================

if st.button("CONVERTIR A AUDIO"):

    if text.strip() == "":
        st.warning("Escribe un texto antes de convertirlo en audio.")

    else:

        result, output_text = text_to_speech(
            text,
            "com",
            lg
        )

        audio_path = f"temp/{result}.mp3"

        with open(audio_path, "rb") as audio_file:

            audio_bytes = audio_file.read()

        st.markdown(
            '<div class="audio-title">Tu audioguía</div>',
            unsafe_allow_html=True
        )

        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )

        # =================================================
        # DESCARGA
        # =================================================

        with open(audio_path, "rb") as f:

            data = f.read()

        bin_str = base64.b64encode(data).decode()

        href = f"""
        <a href="data:audio/mp3;base64,{bin_str}"
           download="{os.path.basename(audio_path)}"
           style="
               display:inline-block;
               margin-top:15px;
               padding:10px 18px;
               border:1px solid #d9a441;
               color:#d9a441;
               text-decoration:none;
               font-family:Poppins,sans-serif;
               font-size:13px;
           ">
           Descargar audioguía
        </a>
        """

        st.markdown(
            href,
            unsafe_allow_html=True
        )


# =========================================================
# LIMPIEZA DE ARCHIVOS ANTIGUOS
# =========================================================

def remove_files(n):

    mp3_files = glob.glob("temp/*mp3")

    if len(mp3_files) != 0:

        now = time.time()
        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                os.remove(f)


remove_files(7)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        MUSEO DEL LOUVRE · AUDIOGUÍA DIGITAL
    </div>
    """,
    unsafe_allow_html=True
)
