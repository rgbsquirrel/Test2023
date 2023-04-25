import cv2
import numpy as np
import streamlit as st
import time

# Define Streamlit app title
st.title("Object Remover")

# Upload an image file
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the uploaded image file
    img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Display the original image
    st.subheader("Original Image")
    st.image(img, channels="BGR", use_column_width=True)

    # Create a copy of the original image for editing
    edited_img = np.copy(img)

    # Define the mask for object removal
    mask = np.zeros_like(edited_img, dtype=np.uint8)

    # Function to remove object from image
    def remove_object(edited_img, mask):
        mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(mask_gray, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            edited_img[y:y + h, x:x + w] = cv2.inpaint(edited_img, contour, 5, cv2.INPAINT_TELEA)
        return edited_img

    # Create a slider to adjust brush size
    brush_size = st.slider("Brush Size", min_value=1, max_value=50, step=1, value=10)

    # Create a color picker to select the object removal color
    color = st.color_picker("Object Color", value="#000000")

    # Convert the color to BGR format
    color_bgr = np.array(st.color_converter.to_rgb(color)) * 255
    color_bgr = color_bgr.astype(np.uint8)

    # Create a checkbox to toggle object removal
    remove_object_checkbox = st.checkbox("Remove Object")

    # Display the edited image
    st.subheader("Edited Image")
    st.image(edited_img, channels="BGR", use_column_width=True)

    # Main loop for object removal
    while remove_object_checkbox:
        # Get mouse event and coordinates
        event = st.get_last_mouse_event()
        x, y = int(event["x"]), int(event["y"])

        # Check if the mouse is within the image bounds
        if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
            # Draw a circle on the mask to mark the area for object removal
            cv2.circle(mask, (x, y), brush_size, color_bgr, -1)

            # Update the edited image with the object removal
            edited_img = remove_object(edited_img, mask)

        # Display the updated edited image
        st.image(edited_img, channels="BGR", use_column_width=True)

        # Wait for a short duration to control the loop speed
        time.sleep(0.01)

        # Check if the remove object checkbox is unchecked
        if not remove_object_checkbox:
            # Reset the mask
            mask = np.zeros_like(edited_img, dtype=np.uint8
# Check if the remove object checkbox is unchecked
if not remove_object_checkbox:
    # Reset the mask
    mask = np.zeros_like(edited_img, dtype=np.uint8)

    # Clear the canvas
    st.canvas_clear()

# Display the final edited image after object removal
st.subheader("Final Edited Image")
st.image(edited_img, channels="BGR", use_column_width=True)
