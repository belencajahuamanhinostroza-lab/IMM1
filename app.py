import streamlit as st
import os
import time
import glob
import base64
from gtts import gTTS
from PIL import Image

# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="Museo del Louvre",
    page_icon="🏛️",
    layout="wide"
)

# ==================================================
# ESTILOS
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Poppins:wght@300;400;500;600&display=swap');

/* ==================================================
   FONDO
   ================================================== */

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
    color: #ffffff;
}

/* ==================================================
   CONTENEDOR
   ================================================== */

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

/* ==================================================
   TIPOGRAFÍA
   ================================================== */

/* TÍTULOS CON SERIFAS */

h1, h2, h3,
.museum-title,
.art-title,
.audio-title {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
}

/* PÁRRAFOS E INTERFAZ */

.stApp p,
.stApp label,
.stApp span,
.stApp textarea,
.stApp input,
.stApp button,
.stApp select,
.art-description,
.museum-subtitle,
.art-subtitle,
.footer,
.download-link {
    font-family: 'Poppins', sans-serif !important;
}

/* ==================================================
   TÍTULO PRINCIPAL
   ================================================== */

.museum-title {
    text-align: center;
    font-size: 42px;
    font-weight: 600;
    letter-spacing: 6px;
    color: #ffffff;
    margin-top: 10px;
    margin-bottom: 3px;
}

/* ==================================================
   SUBTÍTULO PRINCIPAL
   ================================================== */

.museum-subtitle {
    text-align: center;
    font-size: 14px;
    font-weight: 400;
    color: #d6b36a !important;
    letter-spacing: 1px;
    margin-bottom: 25px;
}

/* ==================================================
   LÍNEA DORADA
   ================================================== */

.gold-line {
    height: 1px;
    width: 130px;

    background: linear-gradient(
        90deg,
        transparent,
        #d6b36a,
        transparent
    );

    margin: 0 auto 45px auto;
}

/* ==================================================
   SIDEBAR
   ================================================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #100804 0%,
            #261308 45%,
            #100704 100%
        );

    border-right: 1px solid rgba(214,179,106,0.25);
}

/* Título sidebar */

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    color: #d6b36a !important;
    font-size: 22px;
    letter-spacing: 2px;
}

/* Textos sidebar */

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff !important;
}

/* ==================================================
   TÍTULO DE LA OBRA
   ================================================== */

.art-title {
    font-size: 34px;
    font-weight: 600;
    letter-spacing: 2px;
    color: #ffffff;
    margin-bottom: 2px;
}

/* ==================================================
   SUBTÍTULO DE LA OBRA
   ================================================== */

.art-subtitle {
    font-size: 14px;
    font-weight: 400;
    color: #d6b36a !important;
    letter-spacing: 0.5px;
    margin-bottom: 22px;
}

/* ==================================================
   PÁRRAFO
   ================================================== */

.art-description {
    font-size: 15px;
    font-weight: 300;
    line-height: 1.9;
    color: #ffffff !important;
    text-align: justify;
}

/* ==================================================
   MARCO DE LA IMAGEN
   ================================================== */

.image-frame {
    padding: 8px;

    background:
        linear-gradient(
            145deg,
            #d6b36a,
            #74552d,
            #d6b36a
        );

    box-shadow:
        0 18px 50px rgba(0,0,0,0.60);
}

/* ==================================================
   AUDIOGUÍA
   ================================================== */

.audio-title {
    font-size: 25px;
    font-weight: 600;
    letter-spacing: 2px;
    color: #d6b36a !important;
    margin-top: 35px;
}

/* ==================================================
   TEXTO DE INDICACIÓN
   ================================================== */

.audio-description {
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff !important;
    font-size: 14px;
    font-weight: 300;
}

/* ==================================================
   TEXT AREA
   ================================================== */

.stTextArea textarea {
    background: rgba(8,5,3,0.75) !important;
    color: #ffffff !important;

    border: 1px solid rgba(214,179,106,0.35) !important;

    border-radius: 3px !important;

    font-family: 'Poppins', sans-serif !important;

    font-size: 14px !important;
}

.stTextArea textarea:focus {
    border: 1px solid #d6b36a !important;

    box-shadow:
        0 0 12px rgba(214,179,106,0.15) !important;
}

/* Placeholder */

.stTextArea textarea::placeholder {
    color: rgba(255,255,255,0.75) !important;
}

/* ==================================================
   LABELS
   ================================================== */

label,
[data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
    font-family: 'Poppins', sans-serif !important;
}

/* ==================================================
   SELECTBOX
   ================================================== */

div[data-baseweb="select"] > div {
    background: rgba(8,5,3,0.80) !important;

    border: 1px solid rgba(214,179,106,0.35) !important;
}

div[data-baseweb="select"] * {
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff !important;
}

/* ==================================================
   BOTÓN
   ================================================== */

.stButton > button {
    width: 100%;

    background:
        linear-gradient(
            135deg,
            #d6b36a,
            #a47b38
        );

    color: #090604 !important;

    border: none;

    border-radius: 3px;

    padding: 12px 25px;

    font-family: 'Poppins', sans-serif !important;

    font-size: 13px;

    font-weight: 600;

    letter-spacing: 1.2px;

    transition: all 0.3s ease;
}

.stButton > button:hover {
    background:
        linear-gradient(
            135deg,
            #e4c77e,
            #bd934b
        );

    box-shadow:
        0 8px 25px rgba(214,179,106,0.20);

    transform: translateY(-1px);
}

/* ==================================================
   AUDIO
   ================================================== */

audio {
    width: 100%;
    margin-top: 10px;
}

/* ==================================================
   DIVISOR
   ================================================== */

hr {
    border: none;

    height: 1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(214,179,106,0.35),
            transparent
        );

    margin: 45px 0;
}

/* ==================================================
   LINK DE DESCARGA
   ================================================== */

.download-link {
    display: inline-block;

    margin-top: 15px;

    padding: 10px 18px;

    border: 1px solid rgba(214,179,106,0.50);

    color: #d6b36a !important;

    text-decoration: none;

    font-size: 12px;

    letter-spacing: 1px;

    transition: 0.3s;
}

.download-link:hover {
    background: rgba(214,179,106,0.10);

    border-color: #d6b36a;
}

/* ==================================================
   FOOTER
   ================================================== */

.footer {
    text-align: center;

    margin-top: 70px;

    color: #ffffff !important;

    font-size: 10px;

    letter-spacing: 2px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# ENCABEZADO
# ==================================================

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


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown("### AUDIOGUÍA")

    st.markdown(
        """
        <p style="
        color:#ffffff;
        line-height:1.8;
        font-family:Poppins,sans-serif;
        font-size:14px;
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
        color:#ffffff;
        font-family:Poppins,sans-serif;
        font-size:10px;
        letter-spacing:1.5px;
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
        font-family:Poppins,sans-serif;
        font-size:16px;
        ">
        Leonardo da Vinci
        </p>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# IMAGEN
# ==================================================

image = Image.open("monalisa.jpg")


# ==================================================
# OBRA
# ==================================================

col1, col2 = st.columns(
    [0.95, 1.25],
    gap="large"
)


# ==================================================
# IMAGEN
# ==================================================

with col1:

    st.markdown(
        '<div class="image-frame">',
        unsafe_allow_html=True
    )

    st.image(
        image,
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ==================================================
# INFORMACIÓN
# ==================================================

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


# ==================================================
# AUDIOGUÍA
# ==================================================

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    '<div class="audio-title">AUDIOGUÍA DE LA OBRA</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class="audio-description">
    Copia o escribe un texto para convertirlo en una narración.
    </p>
    """,
    unsafe_allow_html=True
)


# ==================================================
# TEXTO
# ==================================================

text = st.text_area(
    "Texto para escuchar",
    height=150,
    placeholder="Escribe aquí el texto de la audioguía..."
)


# ==================================================
# IDIOMA
# ==================================================

option_lang = st.selectbox(
    "Idioma de la audioguía",
    ("Español", "English")
)

if option_lang == "Español":
    lg = "es"
else:
    lg = "en"


# ==================================================
# CARPETA TEMPORAL
# ==================================================

try:
    os.mkdir("temp")
except:
    pass


# ==================================================
# TEXT TO SPEECH
# ==================================================

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


# ==================================================
# BOTÓN
# ==================================================

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

        with open(
            audio_path,
            "rb"
        ) as audio_file:

            audio_bytes = audio_file.read()

        st.markdown(
            '<div class="audio-title">REPRODUCCIÓN</div>',
            unsafe_allow_html=True
        )

        st.audio(
            audio_bytes,
            format="audio/mp3"
        )

        # ==================================================
        # DESCARGA
        # ==================================================

        bin_str = base64.b64encode(
            audio_bytes
        ).decode()

        href = f"""
        <a class="download-link"
           href="data:application/octet-stream;base64,{bin_str}"
           download="{result}.mp3">
           ↓ &nbsp; GUARDAR AUDIO
        </a>
        """

        st.markdown(
            href,
            unsafe_allow_html=True
        )


# ==================================================
# LIMPIEZA
# ==================================================

def remove_files(n):

    mp3_files = glob.glob("temp/*mp3")

    if len(mp3_files) != 0:

        now = time.time()
        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                os.remove(f)


remove_files(7)


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
    MUSÉE DU LOUVRE · PARIS · DIGITAL AUDIO GUIDE
    </div>
    """,
    unsafe_allow_html=True
)
