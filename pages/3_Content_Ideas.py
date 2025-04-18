import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import requests
from datetime import datetime

def app():
    # 🔐 Access control
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Please log in to access this feature.")
        return

    st.title("📌 AI Content Idea Generator for Delicacy")
    st.markdown("Generate social media ideas based on local food trends and AI strategy.")

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

    # Initialize the Groq LLaMA model
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="groq/llama-3.3-70b-versatile"
    )

    def get_real_time_trends(location):
        """Fetches real-time food-related trends for the given location."""
        url = "https://serper-api.com/search"
        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
        params = {"q": f"{location} trending food news", "num": 5}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return [item["title"] for item in response.json().get("organic", [])]
            return ["⚠️ No trending topics found."]
        except Exception as e:
            return [f"Error fetching trends: {str(e)}"]

    content_agent = Agent(
        role="Content Strategist",
        goal="Provide engaging content suggestions for restaurant owners based on trends.",
        backstory="An AI-powered marketing assistant that helps Delicacy generate social media content ideas using local trends and creativity.",
        llm=llm,
        verbose=True
    )

    location = st.text_input("📍 Enter your city or area for localized content:")

    if st.button("✨ Get Content Suggestions"):
        if location:
            trends = get_real_time_trends(location)
            prompt = f"Generate 5-7 unique and engaging social media content ideas for Delicacy Restaurant based on these trends: {trends}"

            # Create a content generation task
            content_task = Task(
                description=prompt,
                agent=content_agent,
                expected_output="A list of 5-7 engaging content ideas for restaurant marketing based on current trends."
            )

            crew = Crew(
                agents=[content_agent],
                tasks=[content_task],
                process=Process.sequential
            )

            with st.spinner("Thinking like a marketing guru..."):
                result = crew.kickoff()

                today = datetime.now().strftime("%B %d, %Y")
                content = getattr(result, 'raw', result)

                if isinstance(content, str):
                    content = content.strip('"').replace('\\"', '"').replace('\\n', '\n')

                st.markdown(f"## 💡 Content Ideas for {location} ({today})")
                st.markdown(content)
        else:
            st.warning("Please enter a location to generate content ideas.")

app()