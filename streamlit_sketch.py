import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import cv2
from io import BytesIO

# Set custom page config
st.set_page_config(
    page_title="Image Effects Converter",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    h1 {
        color: #4a4a4a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
    }
    .stFileUploader > label {
        font-size: 1.2rem;
        color: #555555;
        font-weight: 600;
    }
    .stSelectbox > label {
        font-size: 1.1rem;
        color: #555555;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        font-size: 1rem;
        border-radius: 8px;
        border: none;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Image processing functions
def convert_to_sketch(image: Image.Image, effect_type: str) -> Image.Image:
    if effect_type == "Pencil Sketch ":
        gray_image = image.convert('L')
        gray_np = np.array(gray_image)
        inverted_gray = cv2.bitwise_not(gray_np)
        blurred = cv2.GaussianBlur(inverted_gray, (21, 21), 0)
        sketch = cv2.divide(gray_np, 255 - blurred, scale=256)
        return Image.fromarray(sketch)

    elif effect_type == "Contour Sketch":
        edge_image = image.filter(ImageFilter.CONTOUR)
        return edge_image

# Main title
st.markdown("<h1>🎨 Image To Sketch </h1>", unsafe_allow_html=True)

# Upload and conversion options
uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png","webp"])
conversion_type = st.selectbox("Choose the effect", ["Pencil Sketch ", "Contour Sketch"])

# Display the original and converted images side by side
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Convert image
    converted_image = convert_to_sketch(image, conversion_type)

    # Display images side by side
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Original Image", use_column_width=True)

    with col2:
        st.image(converted_image, caption=f"{conversion_type} Image", use_column_width=True)

    # Save the converted image to a BytesIO buffer
    buf = BytesIO()
    converted_image.save(buf, format="PNG")
    buf.seek(0)

    # Add download button
    st.download_button(
        label="Download Image",
        data=buf,
        file_name="converted_image.png",
        mime="image/png",
    )
else:
    st.write("Please upload an image to apply effects.")

# Footer
st.markdown(
    """
    <div style="text-align: center; padding: 10px; margin-top: 50px;">
    <small>Created with ❤️ using Streamlit</small>
    </div>
    """,
    unsafe_allow_html=True,
)
