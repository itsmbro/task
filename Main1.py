import streamlit as st
from PIL import Image
from moviepy.editor import ImageSequenceClip
import tempfile

st.set_page_config(page_title="Crea Video da Foto", layout="centered")

st.title("📸 Genera un Video da Foto")
st.write("Carica le tue immagini per creare un video scaricabile.")

uploaded_files = st.file_uploader("Carica immagini", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"{len(uploaded_files)} immagini caricate.")

    if st.button("🎬 Crea Video"):
        with st.spinner("Generazione video in corso..."):

            # Ordina le immagini per nome (opzionale)
            uploaded_files.sort(key=lambda x: x.name)

            # Carica immagini come array
            images = []
            for file in uploaded_files:
                img = Image.open(file).convert("RGB")
                images.append(img)

            # Uniforma dimensioni (tutte come la prima immagine)
            base_size = images[0].size
            resized_images = [img.resize(base_size) for img in images]

            # Salva immagini in una directory temporanea
            temp_dir = tempfile.mkdtemp()
            image_paths = []
            for idx, img in enumerate(resized_images):
                path = f"{temp_dir}/frame_{idx:03d}.png"
                img.save(path)
                image_paths.append(path)

            # Crea il video: 10 fps → 0.1 sec per immagine
            clip = ImageSequenceClip(image_paths, fps=10)

            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            clip.write_videofile(temp_video.name, codec="libx264", audio=False)

        st.success("✅ Video generato!")

        with open(temp_video.name, "rb") as f:
            video_bytes = f.read()
            st.video(video_bytes)
            st.download_button(
                label="📥 Scarica il Video",
                data=video_bytes,
                file_name="slideshow.mp4",
                mime="video/mp4"
            )
