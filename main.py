import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Delicacy Restaurant Marketing Suite",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🍽️ Welcome to Delicacy Restaurant Marketing Suite!")
st.markdown("""
Use the sidebar to navigate through the tools:

- **Social Media Posts** 📣  
- **Image Generator** 🎨  
- **Content Ideas** 💡  
- **Image Captions** 🖼️

Start creating engaging and delicious content for your audience!
""")
