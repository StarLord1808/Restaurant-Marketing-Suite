#2_Image_Generator.py
import streamlit as st
from together import Together
import requests
from io import BytesIO
import os

def app():
    # Access control
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Please log in to access this page.")
        return

    st.header("📸 Delicacy Restaurant Image Generator")
    st.write("Generate custom food and ambiance images using AI for menus, promotions, and posts.")

    st.sidebar.title("🖼️ Prompt Examples")
    st.sidebar.markdown("""
    _Describe the food, vibe, or scene you'd like._

    **Examples:**
    - A gourmet plate of Delicacy's signature seafood pasta with garnish.
    - Cozy night ambiance of Delicacy with candles.
    - A chef plating food in an open kitchen.
    """)

    # Get API key from env
    api_key = os.environ.get("TOGETHER_API_KEY")
    if not api_key:
        st.error("Missing TOGETHER_API_KEY in environment.")
        return

    client = Together(api_key=api_key)

    def generate_image(prompt, model="black-forest-labs/FLUX.1-schnell-Free", steps=4):
        try:
            if "Delicacy" not in prompt.lower():
                prompt = f"Delicacy Restaurant: {prompt}"
            response = client.images.generate(prompt=prompt, model=model, steps=steps)
            return response.data[0].url
        except Exception as e:
            st.error(f"Error generating image: {e}")
            return None

    def download_image(image_url):
        response = requests.get(image_url)
        return BytesIO(response.content)

    prompt = st.text_input("🎨 Describe your image:")
    st.caption("E.g., 'A beautifully plated signature dish', 'Chef in action in open kitchen'")

    if st.button("Generate Restaurant Image"):
        if prompt:
            with st.spinner("🧠 Generating your image..."):
                image_url = generate_image(prompt)
                if image_url:
                    st.image(image_url, caption="Generated Delicacy Image", width=500)
                    img_data = download_image(image_url)
                    st.download_button(
                        label="⬇️ Download Image",
                        data=img_data,
                        file_name="Sappuda_Vanga_Image.png",
                        mime="image/png",
                    )
        else:
            st.warning("Please enter a description to generate the image.")

    st.markdown("---")
    st.info("✨ Powered by the Delicacy AI Marketing Team")

app()