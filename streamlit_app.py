import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(page_title="🤗💬 Let's Chat")

# Hugging Face Credentials
with st.sidebar:
    st.title("🤗💬 Let's Chat")
    
    # Check if credentials are already in Streamlit secrets
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        # Let user input credentials manually if not provided in secrets
        hf_email = st.text_input('Enter E-mail:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    
    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!')

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    try:
        # Check if login cookies are already saved in session_state
        if "cookies" not in st.session_state:
            # Hugging Face Login
            sign = Login(email, passwd)
            cookies = sign.login()
            st.session_state.cookies = cookies.get_dict()  # Save cookies to session_state
        else:
            cookies = st.session_state.cookies
        
        # Create ChatBot
        chatbot = hugchat.ChatBot(cookies=cookies)
        return chatbot.chat(prompt_input)
    
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "I'm sorry, there was an issue with the request. Please try again."

# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_pass)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)