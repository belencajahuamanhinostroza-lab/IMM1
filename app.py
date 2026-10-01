import streamlit as st
import os
import time
import glob
import base64

from gtts import gTTS
from PIL import Image


# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Museo del Louvre",
    page_icon="🏛️",
    layout="wide"
)


# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

/* ---------- FONDO GENERAL ---------- */

.stApp {
    background-color: #0b0b0b;
    color: #eeeeee;
}


/* ---------- TÍTULOS ---------- */

h1, h2, h3 {
    font-family: Arial, Helvetica, sans-serif !important;
    color: #d4af37 !important;
    letter-spacing: 1px;
}


/* ---------- TEXTO NORMAL ---------- */

p, label, .stMarkdown {
    color: #dddddd;
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.7;
}


/* ---------- TÍTULO PRINCIPAL ---------- */

.museum-title {
    text-align: center;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 48px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #d4af37;
    margin-top: 10px;
    margin-bottom: 5px;
}

.museum-subtitle {
    text-align: center;
    color: #aaa;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 17px;
    margin-bottom: 35px;
}


/* ---------- LÍNEA DORADA ---------- */

.gold-line {
    height: 2px;
    background: #d4af37;
    width: 80%;
    margin: 10px auto 30px auto;
}


/* ---------- TARJETAS ---------- */

.museum-card {
    background-color: #151515;
    border: 1px solid #8f7424;
    padding: 25px;
    border-radius: 4px;
    margin-bottom: 25px;
}


/* ---------- IMAGEN ---------- */

.image-frame {
    border: 1px solid #d4af37;
    padding: 8px;
    background-color: #111111;
}


/* ---------- BOTONES ---------- */

.stButton > button {
    background-color: #d4af37;
    color: #080808;
    border: none;
    border-radius: 3px;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: bold;
    padding: 10px 25px;
}

.stButton > button:hover {
    background-color: #f0d66a;
    color: #000000;
}


/* ---------- SELECTBOX Y TEXT AREA ---------- */

.stSelectbox > div > div,
.stTextArea textarea {
    background-color: #171717 !important;
    color: #eeeeee !important;
    border: 1px solid #8f7424 !important;
}


/* ---------- CÁMARA / INPUT ---------- */

.stFileUploader,
[data-testid="stCameraInput"] {
    background-color: #151515;
    border: 1px solid #8f7424;
    border-radius: 4px;
}


/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #8f7424;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #d4af37 !important;
}


/* ---------- AUDIO ---------- */

audio {
    width: 100%;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# CARPETA TEMPORAL
# ==========================================

try:
    os.mkdir("temp")
except:
    pass


# ==========================================
# ENCABEZADO
# ==========================================

st.markdown(
    '<div class="museum-title">MUSEO DEL LOUVRE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="museum-subtitle">'
    'Colección de arte · Leonardo da Vinci'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="gold-line"></div>',
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown(
        "### 🎧 Audioguía",
        unsafe_allow_html=True
    )

    st.write(
        "Escribe o selecciona un texto para escucharlo."
    )

    st.markdown("---")

    st.write(
        "Explora la historia de una de las obras "
        "más reconocidas del arte occidental."
    )


# ==========================================
# IMAGEN PRINCIPAL
# ==========================================

col1, col2 = st.columns([1, 1.4])


with col1:

    image = Image.open("monalisa.jpg")

    st.image(
        image,
        width=350
    )


with col2:

    st.markdown(
        '<h2>La Gioconda</h2>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="museum-card">
        <p>
        La Gioconda o Mona Lisa es una célebre obra pictórica
        al óleo de Leonardo da Vinci, creada en su natal
        Florencia entre los años 1503 y 1506, posiblemente
        continuando hasta aproximadamente 1515 o 1517,
        aunque esta fecha de conclusión tan imprecisa es
        objeto de debate.
        </p>

        <p>
        La teoría más aceptada indica que retrata a
        Lisa Gherardini, la esposa del rico comerciante
        de sedas Francesco del Giocondo, motivo por el cual
        lleva también el nombre de La Gioconda.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# SECCIÓN AUDIO
# ==========================================

st.markdown(
    '<h2>🎧 Audioguía de la obra</h2>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="gold-line"></div>',
    unsafe_allow_html=True
)

st.write(
    "Introduce un texto y conviértelo en una narración "
    "para acompañar tu recorrido por el museo."
)


# ==========================================
# TEXTO
# ==========================================

text = st.text_area(
    "Texto para escuchar",
    placeholder="Escribe aquí el texto que deseas escuchar...",
    height=150
)


# ==========================================
# IDIOMA
# ==========================================

option_lang = st.selectbox(
    "Selecciona el idioma",
    ("Español", "English")
)


if option_lang == "Español":
    lg = "es"
else:
    lg = "en"


# ==========================================
# FUNCIÓN TEXT TO SPEECH
# ==========================================

def text_to_speech(text, lg):

    tts = gTTS(
        text=text,
        lang=lg
    )

    try:
        my_file_name = text[:20]
    except:
        my_file_name = "audio"

    # Evitar caracteres problemáticos
    my_file_name = "".join(
        c for c in my_file_name
        if c.isalnum() or c in (" ", "_", "-")
    )

    if not my_file_name:
        my_file_name = "audio"

    file_path = f"temp/{my_file_name}.mp3"

    tts.save(file_path)

    return my_file_name, text


# ==========================================
# BOTÓN DE AUDIO
# ==========================================

if st.button("🎙️ Convertir a audio"):

    if text.strip() == "":
        st.warning(
            "Escribe un texto antes de convertirlo en audio."
        )

    else:

        result, output_text = text_to_speech(
            text,
            lg
        )

        audio_file = open(
            f"temp/{result}.mp3",
            "rb"
        )

        audio_bytes = audio_file.read()

        st.markdown(
            '<h3>Tu audioguía</h3>',
            unsafe_allow_html=True
        )

        st.audio(
            audio_bytes,
            format="audio/mp3",
            start_time=0
        )


        # ======================================
        # DESCARGAR AUDIO
        # ======================================

        with open(
            f"temp/{result}.mp3",
            "rb"
        ) as f:

            data = f.read()


        def get_binary_file_downloader_html(
            bin_file,
            file_label="Archivo"
        ):

            bin_str = base64.b64encode(
                data
            ).decode()

            href = (
                f'<a href="data:audio/mp3;base64,'
                f'{bin_str}" '
                f'download="{os.path.basename(bin_file)}" '
                f'style="color:#d4af37;'
                f'font-weight:bold;">'
                f'⬇️ Descargar {file_label}'
                f'</a>'
            )

            return href


        st.markdown(
            get_binary_file_downloader_html(
                f"temp/{result}.mp3",
                "audioguía"
            ),
            unsafe_allow_html=True
        )


# ==========================================
# LIMPIAR ARCHIVOS ANTIGUOS
# ==========================================

def remove_files(n):

    mp3_files = glob.glob(
        "temp/*mp3"
    )

    if len(mp3_files) != 0:

        now = time.time()

        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                os.remove(f)


remove_files(7)
