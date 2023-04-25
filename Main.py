import streamlit as st
import cv2
import numpy as np

# Load the image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    img = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    edited_img = np.copy(img)
    mask = np.zeros_like(edited_img, dtype=np.uint8)

    # Display the original image
    st.subheader("Original Image")
    st.image(img, channels="BGR", use_column_width=True)

    # Display the edited image
    st.subheader("Edited Image")
    edited_img = cv2.cvtColor(edited_img, cv2.COLOR_BGR2RGB)
    edited_img = cv2.addWeighted(edited_img, 1, mask, 0.7, 0)
    st.image(edited_img, channels="RGB", use_column_width=True)

    # Remove object checkbox
    remove_object_checkbox = st.checkbox("Remove Object")

    if remove_object_checkbox:
        # Add instructions for object removal
        st.info("Click and drag on the image to mark the object to be removed.")

        # Create a canvas for user to mark the object
        canvas_result = st_canvas(
            255 * mask[:, :, 0],
            height=img.shape[0],
            width=img.shape[1],
            drawing_mode="freedraw",
            key="canvas",
        )

        # Get the updated mask
        mask = canvas_result.image_data.astype(np.uint8)[:, :, 0]

        # Apply the mask to the edited image
        edited_img = cv2.cvtColor(edited_img, cv2.COLOR_RGB2BGR)
        edited_img = cv2.addWeighted(edited_img, 1, mask, 0.7, 0)
        edited_img = cv2.cvtColor(edited_img, cv2.COLOR_BGR2RGB)

    # Display the final edited image after object removal
    st.subheader("Final Edited Image")
    st.image(edited_img, channels="RGB", use_column_width=True)
