import os
import cv2
import numpy as np
import streamlit as st
from PIL import Image

def remove_background(uploaded_file, background_color):
    # Save the uploaded file temporarily
    image_path = "temp_image.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert the image to RGB format (required by PIL)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Create a mask to identify the background using a simple threshold
    _, mask = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 240, 255, cv2.THRESH_BINARY)
    
    # Invert the mask to select the foreground
    mask_inv = cv2.bitwise_not(mask)
    
    # Create a white background image
    background = np.full_like(image_rgb, background_color, dtype=np.uint8)
    
    # Extract the foreground using the mask
    foreground = cv2.bitwise_and(image_rgb, image_rgb, mask=mask_inv)
    
    # Combine the foreground and background
    result = cv2.add(background, foreground)
    
    # Convert the result to PIL Image
    result_image = Image.fromarray(result)
    
    # Remove the temporary image file
    os.remove(image_path)
    
    return result_image

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def main():
    st.title("Background Remover App")

    # Upload image through Streamlit
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

        # Choose background color using Streamlit color picker
        background_color = st.color_picker("Choose a background color", "#00ff00")

        if st.button("Remove Background"):
            # Perform background removal
            result_image = remove_background(uploaded_file, hex_to_rgb(background_color))
            
            # Display the result
            st.image(result_image, caption="Result", use_column_width=True)

if __name__ == "__main__":
    main()
