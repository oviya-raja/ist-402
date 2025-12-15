
import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

@st.cache_resource
def load_model():
    '''
    Load BLIP model and processor.
    Cached to avoid reloading on every interaction.
    First run downloads the model (~1GB).
    '''
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

processor, model = load_model()

st.title("🖼️ Image to Caption Generator (BLIP Model)")
st.markdown("Upload an image to generate an automatic caption using AI.")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"], 
                                 help="Supported formats: JPG, JPEG, PNG")

if uploaded_file is not None:
    # Load and display image
    image = Image.open(uploaded_file).convert("RGB")  # Convert to RGB for compatibility
    st.image(image, caption="Uploaded Image")

    # Generate caption
    with st.spinner("Generating caption..."):
        inputs = processor(image, return_tensors="pt")  # Preprocess image
        out = model.generate(**inputs)  # Generate caption tokens
        caption = processor.decode(out[0], skip_special_tokens=True)  # Decode to text

    st.subheader("📝 Generated Caption:")
    st.success(caption)

    # Additional info
    st.caption("💡 Tip: Try different types of images (nature, objects, people, scenes) to see the model's capabilities!")
