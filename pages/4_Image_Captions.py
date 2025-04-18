import streamlit as st
from groq import Groq
import base64
import os
from PIL import Image

def app():
    # 🔐 Auth check
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Please log in to access this feature.")
        return

    # Init Groq client
    client = Groq()
    vision_model = 'meta-llama/llama-4-scout-17b-16e-instruct'

    st.title("🖼️ Delicacy | Image-Based Social Media Generator")
    st.markdown("Upload an image and generate beautiful, engaging social media posts tailored for Delicacy Restaurant.")

    # Function to encode image
    def encode_image_file(image_file):
        return base64.b64encode(image_file.getvalue()).decode('utf-8')

    # Marketing Content Generator
    def generate_marketing_content(client, model, base64_image, extra_details=""):
        prompt = f"""
        You are the owner of Delicacy Restaurant creating a social media post. 
        Analyze this image and write a short, creative caption in the **first-person** voice (I/we/our).

        --- 
        🏪 Restaurant Details:
        Name: Delicacy Restaurant  
        Address: 123 Culinary Street, Foodville  
        Phone: (555) 123-4567  
        Email: info@sappuda-vanga.com  

        🕐 Hours:
        - Mon–Thu: 11am–10pm  
        - Fri–Sat: 11am–11pm  
        - Sun: 10am–9pm  
        ---

        {f"📌 Extra Details: {extra_details}" if extra_details else ""}

        🔖 Caption Requirements:
        1. Eye-catching headline with emojis  
        2. Warm, friendly tone  
        3. Use paragraph breaks and emojis  
        4. End with a strong call-to-action  
        5. Include relevant hashtags  
        6. Naturally mention restaurant details  
        """

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model=model
        )
        return response.choices[0].message.content

    # Upload + Extra Details
    uploaded_file = st.file_uploader("📤 Upload a dish or ambiance image", type=["jpg", "jpeg", "png"])
    extra_details = st.text_area("📝 Any extra context to add?", placeholder="E.g., Ingredients, chef story, special deal")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Your Uploaded Image", use_container_width=True)

        if st.button("✨ Generate Caption"):
            with st.spinner("Cooking up your content..."):
                try:
                    base64_image = encode_image_file(uploaded_file)
                    result = generate_marketing_content(client, vision_model, base64_image, extra_details)

                    st.success("✅ Post Created Successfully!")
                    st.subheader("📣 Suggested Caption")
                    st.write(result)

                except Exception as e:
                    st.error(f"🚫 Error generating content: {str(e)}")

app()