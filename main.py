import PyPDF2
from huggingface_hub import InferenceClient
import streamlit as st
from streamlit_chat import message
from langchain.memory import ConversationBufferWindowMemory
import random

aa=["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","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","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"]
bb=random.choice(aa)

# Hardcoded credentials (Replace with a secure method in production)
VALID_USER_ID = "ailite"
VALID_PASSWORD = "12345qwert"

# Function to check login credentials
def check_login(user_id, password):
    return user_id == VALID_USER_ID and password == VALID_PASSWORD

# Streamlit UI for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.subheader("Login to AiLite ChatBot")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_login(user_id, password):
            st.session_state['logged_in'] = True
            st.success("Login successful!")
        else:
            st.error("Invalid User ID or Password. Please try again.")

else:
    # Open and read the PDF file
    with open('am_2.pdf', 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        all_text = "".join(page.extract_text() for page in reader.pages)

    # System message setup
    data = f'{all_text}. My elder brother is CV Pro.'
    system_content = (
        "You are a helpful AI assistant. You will be given knowledge and need to answer questions strictly based on that document. "
        "If any question is asked out of the text, just answer: 'I apologize for the inconvenience, but I only have information about AiLite in Python. "
        "For further details, please visit our website at https://www.robotixedu.com/'. "
        "Don't reveal that you are answering based on the document provided. Here is your data: " + data
    )

    # Initialize Hugging Face Inference Client (✅ Fixed)
    client = InferenceClient(api_key=bb)  # Replace with your Hugging Face API key

    # Streamlit UI for chatbot
    st.subheader("AiLite ChatBot")

    # Initialize session state for storing chat history and memory
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if 'buffer_memory' not in st.session_state:
        st.session_state.buffer_memory = ConversationBufferWindowMemory(k=100, return_messages=True)

    # Display chat history
    for i, chat in enumerate(st.session_state['chat_history']):
        message(chat['content'], is_user=chat['role'] == 'user', key=f"message_{i}")

    # User input for question
    user_prompt = st.chat_input("Ask anything about me...")

    if user_prompt:
        # Store user's question
        st.session_state['chat_history'].append({"role": "user", "content": user_prompt})
        message(user_prompt, is_user=True, key=f"user_message_{len(st.session_state['chat_history'])}")

        # Generate response using Hugging Face API
        assistant_response = client.text_generation(
            model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",  # Ensure model availability on HF
            prompt=f"{system_content}\nUser: {user_prompt}\nAssistant:",
            max_new_tokens=1000
        )
        assistant_response1=assistant_response.split("</think>")
        assistant_response2=assistant_response1[1]
        # Store and display response
        st.session_state['chat_history'].append({"role": "assistant", "content": assistant_response2})
        message(assistant_response2, key=f"assistant_message_{len(st.session_state['chat_history'])}")
