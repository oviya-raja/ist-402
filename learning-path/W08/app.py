
import streamlit as st
import torch
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import time

# Config
st.set_page_config(page_title="🎙️ Audio-to-Image", layout="centered")

# ==================== Load Models ====================
@st.cache_resource
def load_models():
    """
    Load both Whisper (speech-to-text) and Stable Diffusion (text-to-image) models.
    Models are cached to avoid reloading on every interaction.
    First run takes 3-5 minutes to download models.
    """
    st.info("Loading AI models... (first run takes 3-5 minutes)")

    # Whisper for speech-to-text
    whisper = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-tiny",
        device=0 if torch.cuda.is_available() else -1
    )

    # Stable Diffusion for image generation
    device = "cuda" if torch.cuda.is_available() else "cpu"
    sd = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        safety_checker=None
    ).to(device)

    if device == "cuda":
        sd.enable_attention_slicing()

    return whisper, sd

whisper_model, sd_model = load_models()

# ==================== UI ====================
st.title("🎙️ Audio-to-Image Generator")
st.markdown("Transform your voice into stunning AI-generated images!")
st.markdown("---")

# Input methods
tab1, tab2 = st.tabs(["🎤 Upload Audio", "✍️ Type Text"])

prompt_text = None

with tab1:
    st.write("Upload an audio file with your image description")
    audio_file = st.file_uploader(
        "Choose audio file",
        type=["wav", "mp3", "m4a", "flac"],
        help="Speak clearly: 'A beautiful sunset over mountains'")

    if audio_file:
        st.audio(audio_file)

        if st.button("🎧 Transcribe Audio", type="primary"):
            with st.spinner("Converting speech to text..."):
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_file.read())
                result = whisper_model("temp_audio.wav")
                prompt_text = result["text"]
                st.success(f"✅ Transcription: **{prompt_text}**")
                st.session_state.prompt = prompt_text

with tab2:
    manual_prompt = st.text_area(
        "Describe the image you want to generate:",
        placeholder="Example: A serene lake surrounded by autumn trees at sunset",
        height=100
    )
    if manual_prompt:
        st.session_state.prompt = manual_prompt

# Settings
with st.expander("⚙️ Advanced Settings"):
    col1, col2 = st.columns(2)
    steps = col1.slider("Quality (inference steps)", 10, 50, 25,
                       help="More steps = better quality but slower")
    guidance = col2.slider("Prompt strength", 5.0, 15.0, 7.5,
                          help="Higher = follows prompt more closely")

# Generate button
st.markdown("---")
if st.button("🎨 Generate Image", type="primary", use_container_width=True):
    final_prompt = st.session_state.get('prompt', None)

    if not final_prompt:
        st.error("❌ Please provide audio or text first!")
        st.stop()

    st.info(f"🎨 Generating image from: **{final_prompt}**")
    st.write("This may take 30 seconds to 3 minutes depending on your GPU...")

    progress_bar = st.progress(0)
    start_time = time.time()

    with st.spinner("Creating your masterpiece..."):
        try:
            image = sd_model(
                prompt=final_prompt,
                num_inference_steps=steps,
                guidance_scale=guidance,
                height=512,
                width=512
            ).images[0]

            elapsed = time.time() - start_time
            progress_bar.progress(100)

            st.success(f"✅ Generated in {elapsed:.1f} seconds!")
            st.image(image, caption=final_prompt)

            image.save("generated_image.png")
            with open("generated_image.png", "rb") as f:
                st.download_button(
                    "💾 Download Image",
                    data=f,
                    file_name=f"ai_art_{int(time.time())}.png",
                    mime="image/png",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ Generation failed: {str(e)}")
            st.info("Try simplifying your prompt or reducing quality settings")

# Footer
st.markdown("---")
st.caption("🔊 Powered by OpenAI Whisper + Stable Diffusion v1.5")
device_info = "🚀 GPU Accelerated" if torch.cuda.is_available() else "🐢 CPU Mode (slower)"
st.caption(device_info)
