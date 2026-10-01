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

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

/* ==================================================
   FONDO GENERAL
   ================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 10% 15%,
            rgba(183, 119, 48, 0.38) 0%,
            rgba(183, 119, 48, 0.12) 22%,
            transparent 45%
        ),
        radial-gradient(
            circle at 90% 80%,
            rgba(126, 38, 52, 0.42) 0%,
            rgba(126, 38, 52, 0.15) 25%,
            transparent 52%
        ),
        linear-gradient(
            120deg,
            #020202 0%,
            #170907 18%,
            #451914 40%,
            #2b1111 58%,
            #16090a 78%,
            #010101 100%
        );

    background-attachment: fixed;
    color: #ffffff;
}

/* ==================================================
   TIPOGRAFÍA GENERAL
   ================================================== */

.stApp,
.stApp p,
.stApp label,
.stApp span,
.stApp div,
.stApp textarea,
.stApp input,
.stApp button,
.stApp select {
    font-family: 'Poppins', sans-serif !important;
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
   TÍTULO PRINCIPAL
   ================================================== */

.museum-title {
    text-align: center;
    font-family: 'Poppins', sans-serif !important;
    font-size: 38px;
    font-weight: 500;
    letter-spacing: 7px;
    color: #d6b36a;
    margin-top: 10px;
    margin-bottom: 5px;
}

/* ==================================================
   SUBTÍTULO PRINCIPAL
   ================================================== */

.museum-subtitle {
    text-align: center;
    font-family: 'Poppins', sans-serif !important;
    font-size: 15px;
    font-weight: 300;
    color: #ffffff !important;
    margin-bottom: 25px;
}

/* ==================================================
   LÍNEA DORADA
   ================================================== */

.gold-line {
    height: 1px;
    width: 150px;

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
            rgba(8, 4, 4, 0.97),
            rgba(32, 10, 11, 0.97),
            rgba(7, 4, 4, 0.98)
        );

    border-right: 1px solid rgba(214, 179, 106, 0.25);
}

/* Textos sidebar */

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {

    font-family: 'Poppins', sans-serif !important;
    color: #ffffff !important;
}

/* Títulos sidebar */

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {

    color: #d6b36a !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500;
    letter-spacing: 2px;
}

/* ==================================================
   TARJETA DE LA OBRA
   ================================================== */

.art-card {

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.07),
            rgba(255,255,255,0.015)
        );

    border: 1px solid rgba(214,179,106,0.25);

    border-radius: 5px;

    padding: 28px;

    box-shadow:
        0 20px 60px rgba(0,0,0,0.55),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

/* ==================================================
   TÍTULO DE LA OBRA
   ================================================== */

.art-title {

    font-family: 'Poppins', sans-serif !important;

    font-size: 28px;

    font-weight: 500;

    letter-spacing: 3px;

    color: #d6b36a;

    margin-bottom: 5px;
}

/* ==================================================
   SUBTÍTULO DE LA OBRA
   ================================================== */

.art-subtitle {

    font-family: 'Poppins', sans-serif !important;

    font-size: 14px;

    font-weight: 300;

    color: #ffffff !important;

    margin-bottom: 22px;
}

/* ==================================================
   DESCRIPCIÓN
   ================================================== */

.art-description {

    font-family: 'Poppins', sans-serif !important;

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
            #715329,
            #d6b36a
        );

    box-shadow:
        0 18px 50px rgba(0,0,0,0.65);
}

/* ==================================================
   AUDIOGUÍA
   ================================================== */

.audio-title {

    font-family: 'Poppins', sans-serif !important;

    font-size: 18px;

    font-weight: 500;

    letter-spacing: 2px;

    color: #d6b36a !important;

    margin-top: 35px;
}

/* ==================================================
   TEXTAREA
   ================================================== */

.stTextArea textarea {

    background: rgba(5, 4, 4, 0.75) !important;

    color: #ffffff !important;

    border: 1px solid rgba(214,179,106,0.35) !important;

    border-radius: 4px !important;

    font-family: 'Poppins', sans-serif !important;

    font-size: 14px !important;
}

.stTextArea textarea:focus {

    border: 1px solid #d6b36a !important;

    box-shadow:
        0 0 15px rgba(214,179,106,0.15) !important;
}

/* Placeholder */

.stTextArea textarea::placeholder {

    color: rgba(255,255,255,0.65) !important;

    font-family: 'Poppins', sans-serif !important;
}

/* ==================================================
   SELECTBOX
   ================================================== */

div[data-baseweb="select"] > div {

    background: rgba(5,4,4,0.8) !important;

    border: 1px solid rgba(214,179,106,0.35) !important;

    color: #ffffff !important;
}

div[data-baseweb="select"] * {

    font-family: 'Poppins', sans-serif !important;

    color: #ffffff !important;
}

/* ==================================================
   LABELS
   ================================================== */

label,
[data-testid="stWidgetLabel"] p {

    color: #ffffff !important;

    font-family: 'Poppins', sans-serif !important;

    font-weight: 400;
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
            #a47c38
        );

    color: #090807 !important;

    border: none;

    border-radius: 3px;

    padding: 13px 25px;

    font-family: 'Poppins', sans-serif !important;

    font-size: 13px;

    font-weight: 600;

    letter-spacing: 1.5px;

    transition: all 0.3s ease;
}

.stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            #e5c87e,
            #bd934c
        );

    box-shadow:
        0 8px 30px rgba(214,179,106,0.25);

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
            rgba(214,179,106,0.4),
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

    padding: 10px 20px;

    border: 1px solid rgba(214,179,106,0.5);

    color: #d6b36a !important;

    text-decoration: none;

    font-family: 'Poppins', sans-serif !important;

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

    font-family: 'Poppins', sans-serif !important;

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
# INFORMACIÓN DE LA OBRA
# ==================================================

col1, col2 = st.columns(
    [0.95, 1.25],
    gap="large"
)


# ==================================================
# COLUMNA IZQUIERDA
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
# COLUMNA DERECHA
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
    <p style="
    color:#ffffff;
    font-family:Poppins,sans-serif;
    font-size:14px;
    font-weight:300;
    ">
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
# CONVERTIR A AUDIO
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
# LIMPIAR ARCHIVOS ANTIGUOS
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
