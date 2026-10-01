import streamlit as st
import os
import time
import glob
import base64
from gtts import gTTS
from PIL import Image

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Museo del Louvre",
    page_icon="🏛️",
    layout="wide"
)

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Montserrat:wght@300;400;500;600&display=swap');

/* FONDO GENERAL */
.stApp {
    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(119, 82, 35, 0.18) 0%,
            rgba(0, 0, 0, 0) 32%
        ),
        radial-gradient(
            circle at 85% 80%,
            rgba(72, 38, 21, 0.20) 0%,
            rgba(0, 0, 0, 0) 35%
        ),
        linear-gradient(
            135deg,
            #050505 0%,
            #100c09 30%,
            #18110c 55%,
            #0b0908 78%,
            #020202 100%
        );
    color: #eee8dc;
}

/* QUITAR ESPACIO SUPERIOR */
.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

/* TÍTULOS */
h1, h2, h3 {
    font-family: 'Montserrat', sans-serif !important;
    letter-spacing: 2px;
}

/* TEXTO NORMAL */
p, label, .stMarkdown {
    font-family: Georgia, 'Times New Roman', serif;
}

/* TÍTULO PRINCIPAL */
.museum-title {
    text-align: center;
    font-family: 'Montserrat', sans-serif;
    font-size: 38px;
    font-weight: 500;
    letter-spacing: 7px;
    color: #d6b36a;
    margin-top: 10px;
    margin-bottom: 5px;
}

/* SUBTÍTULO */
.museum-subtitle {
    text-align: center;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 17px;
    font-style: italic;
    color: #c8c0b2;
    margin-bottom: 25px;
}

/* LÍNEA DORADA */
.gold-line {
    height: 1px;
    width: 130px;
    background: linear-gradient(
        90deg,
        transparent,
        #c9a45c,
        transparent
    );
    margin: 0 auto 45px auto;
}

/* TARJETA PRINCIPAL */
.art-card {
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.015)
        );
    border: 1px solid rgba(201,164,92,0.25);
    border-radius: 4px;
    padding: 28px;
    box-shadow:
        0 20px 60px rgba(0,0,0,0.45),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

/* TÍTULO DE OBRA */
.art-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 28px;
    font-weight: 500;
    letter-spacing: 3px;
    color: #d6b36a;
    margin-bottom: 5px;
}

/* SUBTÍTULO DE OBRA */
.art-subtitle {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 16px;
    font-style: italic;
    color: #aaa296;
    margin-bottom: 22px;
}

/* TEXTO DE LA OBRA */
.art-description {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 17px;
    line-height: 1.85;
    color: #e1dbcf;
    text-align: justify;
}

/* MARCO DE IMAGEN */
.image-frame {
    padding: 9px;
    background:
        linear-gradient(
            145deg,
            #d1af68,
            #6f542d,
            #d1af68
        );
    box-shadow:
        0 15px 45px rgba(0,0,0,0.65);
}

/* TEXTO DE AUDIO */
.audio-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 18px;
    letter-spacing: 2px;
    color: #d6b36a;
    margin-top: 35px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0b0907 0%,
            #15100b 55%,
            #080706 100%
        );
    border-right: 1px solid rgba(201,164,92,0.18);
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #d6b36a !important;
    font-family: 'Montserrat', sans-serif !important;
    letter-spacing: 2px;
}

/* TEXT AREA */
.stTextArea textarea {
    background: rgba(10,9,8,0.75) !important;
    color: #eee8dc !important;
    border: 1px solid rgba(201,164,92,0.35) !important;
    border-radius: 3px !important;
    font-family: Georgia, 'Times New Roman', serif !important;
    font-size: 16px !important;
}

.stTextArea textarea:focus {
    border: 1px solid #c9a45c !important;
    box-shadow: 0 0 12px rgba(201,164,92,0.12) !important;
}

/* SELECTBOX */
div[data-baseweb="select"] > div {
    background: rgba(10,9,8,0.75) !important;
    border: 1px solid rgba(201,164,92,0.30) !important;
    color: #eee8dc !important;
}

/* BOTÓN */
.stButton > button {
    width: 100%;
    background:
        linear-gradient(
            135deg,
            #c9a45c,
            #9e7939
        );
    color: #090807 !important;
    border: none;
    border-radius: 2px;
    padding: 12px 25px;
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    letter-spacing: 1.5px;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background:
        linear-gradient(
            135deg,
            #e0c27b,
            #b58b45
        );
    box-shadow: 0 8px 25px rgba(201,164,92,0.20);
    transform: translateY(-1px);
}

/* AUDIO */
audio {
    width: 100%;
    margin-top: 10px;
}

/* DIVISOR */
hr {
    border: none;
    height: 1px;
    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(201,164,92,0.35),
            transparent
        );
    margin: 45px 0;
}

/* LINK DE DESCARGA */
.download-link {
    display: inline-block;
    margin-top: 15px;
    padding: 10px 18px;
    border: 1px solid rgba(201,164,92,0.45);
    color: #d6b36a !important;
    text-decoration: none;
    font-family: 'Montserrat', sans-serif;
    font-size: 13px;
    letter-spacing: 1px;
    transition: 0.3s;
}

.download-link:hover {
    background: rgba(201,164,92,0.10);
    border-color: #d6b36a;
}

/* PIE */
.footer {
    text-align: center;
    margin-top: 70px;
    color: #756f66;
    font-family: 'Montserrat', sans-serif;
    font-size: 11px;
    letter-spacing: 2px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

st.markdown(
    '<div class="museum-title">MUSEO DEL LOUVRE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="museum-subtitle">Colección de obras maestras · Audioguía digital</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="gold-line"></div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("### AUDIOGUÍA")

    st.markdown(
        """
        <p style="
        color:#aaa296;
        line-height:1.7;
        font-family:Georgia;
        ">
        Explora la obra y utiliza la audioguía
        para escuchar el contenido seleccionado.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        """
        <p style="
        color:#756f66;
        font-family:Montserrat;
        font-size:11px;
        letter-spacing:1px;
        ">
        COLECCIÓN PERMANENTE
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
        color:#d6b36a;
        font-family:Georgia;
        font-size:16px;
        ">
        Leonardo da Vinci
        </p>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# IMAGEN
# --------------------------------------------------

image = Image.open("monalisa.jpg")


# --------------------------------------------------
# OBRA
# --------------------------------------------------

col1, col2 = st.columns([0.95, 1.25], gap="large")

with col1:

    st.markdown('<div class="image-frame">', unsafe_allow_html=True)
    st.image(image, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col2:

    st.markdown(
        '<div class="art-title">LA MONA LISA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="art-subtitle">La Gioconda · Leonardo da Vinci</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="art-description">
        La Gioconda o Mona Lisa es una célebre obra pictórica
        al óleo de Leonardo da Vinci, creada en su natal Florencia
        entre los años 1503 y 1506, posiblemente continuando hasta
        aproximadamente 1515 o 1517, aunque esta fecha de conclusión
        tan imprecisa es objeto de debate.
        <br><br>
        La teoría más aceptada indica que retrata a Lisa Gherardini,
        esposa del rico comerciante de sedas Francesco del Giocondo,
        motivo por el cual también recibe el nombre de
        <i>La Gioconda</i>.
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# AUDIOGUÍA
# --------------------------------------------------

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    '<div class="audio-title">AUDIOGUÍA DE LA OBRA</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
    color:#aaa296;
    font-family:Georgia;
    font-size:15px;
    ">
    Copia o escribe un texto para convertirlo en una narración.
    </p>
    """,
    unsafe_allow_html=True
)

text = st.text_area(
    "Texto para escuchar",
    height=150,
    placeholder="Escribe aquí el texto de la audioguía..."
)


# --------------------------------------------------
# IDIOMA
# --------------------------------------------------

option_lang = st.selectbox(
    "Idioma de la audioguía",
    ("Español", "English")
)

if option_lang == "Español":
    lg = "es"
else:
    lg = "en"


# --------------------------------------------------
# CARPETA TEMPORAL
# --------------------------------------------------

try:
    os.mkdir("temp")
except:
    pass


# --------------------------------------------------
# TEXT TO SPEECH
# --------------------------------------------------

def text_to_speech(text, lg):

    tts = gTTS(
        text=text,
        lang=lg
    )

    safe_name = "".join(
        c for c in text[:20]
        if c.isalnum() or c in (" ", "_", "-")
    ).strip()

    if not safe_name:
        safe_name = "audio"

    filename = f"temp/{safe_name}.mp3"

    tts.save(filename)

    return safe_name, filename


# --------------------------------------------------
# BOTÓN
# --------------------------------------------------

if st.button("✦  CONVERTIR A AUDIO"):

    if not text.strip():

        st.warning(
            "Escribe un texto antes de generar la audioguía."
        )

    else:

        result, audio_path = text_to_speech(
            text,
            lg
        )

        with open(audio_path, "rb") as audio_file:

            audio_bytes = audio_file.read()

        st.markdown(
            '<div class="audio-title">REPRODUCCIÓN</div>',
            unsafe_allow_html=True
        )

        st.audio(
            audio_bytes,
            format="audio/mp3"
        )

        # --------------------------------------------------
        # DESCARGA
        # --------------------------------------------------

        bin_str = base64.b64encode(
            audio_bytes
        ).decode()

        href = f"""
        <a class="download-link"
           href="data:application/octet-stream;base64,{bin_str}"
           download="{result}.mp3">
           ↓  GUARDAR AUDIO
        </a>
        """

        st.markdown(
            href,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# LIMPIAR ARCHIVOS ANTIGUOS
# --------------------------------------------------

def remove_files(n):

    mp3_files = glob.glob("temp/*mp3")

    if len(mp3_files) != 0:

        now = time.time()
        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                os.remove(f)


remove_files(7)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
    MUSÉE DU LOUVRE · PARIS · DIGITAL AUDIO GUIDE
    </div>
    """,
    unsafe_allow_html=True
)
