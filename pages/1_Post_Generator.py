#1_Post_Generator.py
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

def app():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Please log in to access this page.")
        return

    # Set API keys
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    st.title("📣 Delicacy Restaurant Content Generator")
    st.write("Create engaging content for social media posts.")

    # Initialize the Groq LLaMA model
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="groq/llama-3.3-70b-versatile"
    )

    def create_agents_and_tasks(user_topic):
        restaurant_knowledge_agent = Agent(
            role="Restaurant Knowledge Agent",
            goal="Store detailed information about the restaurant and provide accurate details when requested.",
            backstory="""You are the knowledge keeper for Delicacy Restaurant...""",
            llm=llm,
            verbose=True
        )

        content_creator_agent = Agent(
            role="Content Creator Agent",
            goal="Generate engaging, authentic, and creative marketing content for Instagram and Facebook...",
            backstory="""You specialize in creating captivating social media posts...""",
            llm=llm,
            verbose=True
        )

        restaurant_task = Task(
            description=f"""Provide comprehensive details about the restaurant focusing on {user_topic or 'general information'}.""",
            agent=restaurant_knowledge_agent,
            expected_output="A detailed description of the restaurant."
        )

        content_task = Task(
            description=f"""Craft an engaging Instagram and Facebook post about {user_topic or 'today\'s special dishes'}.""",
            agent=content_creator_agent,
            context=[restaurant_task],
            expected_output="A creative, friendly, visually-appealing post."
        )

        return Crew(
            agents=[restaurant_knowledge_agent, content_creator_agent],
            tasks=[restaurant_task, content_task],
            process=Process.sequential,
            verbose=True
        )

    user_topic = st.text_input(
        "What would you like to create content about?",
        placeholder="E.g., weekend specials, new menu items, happy hour, etc."
    )

    if st.button("Generate Content"):
        if user_topic or st.checkbox("Generate general content"):
            with st.spinner("Generating your content..."):
                crew = create_agents_and_tasks(user_topic)
                result = crew.kickoff()
                st.success("✅ Content Generated!")
                st.text_area("📄 Generated Content:", value=result, height=300)
        else:
            st.warning("Please enter a topic or select 'Generate general content'")

app()