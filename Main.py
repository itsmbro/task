import streamlit as st
import os
import tempfile
from PIL import Image
import cv2
from io import BytesIO

st.set_page_config(page_title="Crea Video da Foto", layout="centered")

st.title("📸 Genera un Video da Foto")
st.write("Carica le tue immagini e crea un video da scaricare.")

# Upload delle immagini
uploaded_files = st.file_uploader("Carica immagini", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} immagini caricate.")

    if st.button("🎬 Crea Video"):
        # Ordina immagini per nome (opzionale)
        uploaded_files.sort(key=lambda x: x.name)

        with st.spinner("Generazione video in corso..."):

            # Crea un file temporaneo per il video
            temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            temp_dir = tempfile.mkdtemp()

            images = []
            for file in uploaded_files:
                img = Image.open(file).convert("RGB")
                images.append(img)

            # Prendi dimensioni dalla prima immagine
            width, height = images[0].size
            frame_size = (width, height)

            video_writer = cv2.VideoWriter(
                temp_video_file.name,
                cv2.VideoWriter_fourcc(*'mp4v'),
                10,  # 10 fps = 1 frame ogni 0.1 secondi
                frame_size
            )

            for img in images:
                img = img.resize(frame_size)
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                video_writer.write(frame)

            video_writer.release()

        st.success("✅ Video generato con successo!")

        # Mostra anteprima e download
        with open(temp_video_file.name, "rb") as f:
            video_bytes = f.read()
            st.video(video_bytes)
            st.download_button(
                label="📥 Scarica il Video",
                data=video_bytes,
                file_name="slideshow.mp4",
                mime="video/mp4"
            )
