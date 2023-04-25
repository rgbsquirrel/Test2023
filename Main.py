import streamlit as st
from PIL import Image
import cv2

# Set page title
st.title("Image Filter App")

# Upload image file
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert uploaded file to PIL.Image
    img = Image.open(uploaded_file)

    # Display original image
    st.image(img, caption="Original Image")

    # Apply grayscale filter
    if st.button("Grayscale"):
        gray_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        st.image(gray_img, caption="Grayscale Image")

    # Apply blur filter
    if st.button("Blur"):
        ksize = st.slider("Kernel size", 1, 31, 5)
        blur_img = cv2.GaussianBlur(np.array(img), (ksize, ksize), 0)
        st.image(blur_img, caption="Blurred Image")

    # Apply edge detection filter
    if st.button("Edge Detection"):
        edges = cv2.Canny(np.array(img), 100, 200)
        st.image(edges, caption="Edge Detected Image")
else:
    st.warning("Please upload an image file.")
