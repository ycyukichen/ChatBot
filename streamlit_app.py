import streamlit as st
import requests

# App title
st.set_page_config(page_title="🤗💬 Let's Chat")

# Hugging Face API Token and model selection
with st.sidebar:
    st.title('🤗💬 HugChat')

    # Get API Token from secrets or user input
    if 'HF_TOKEN' in st.secrets:
        st.success('Hugging Face API Token provided!', icon='✅')
        hf_token = st.secrets['HF_TOKEN']
    else:
        hf_token = st.text_input('Enter Hugging Face API Token:', type='password')
        if not hf_token:
            st.warning('Please enter your Hugging Face API token!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    
    # Model selection dropdown
    model_choice = st.selectbox(
        "Choose a model for text generation:",
        ["gpt2", "openai-community/gpt2", "gpt-neo-2.7B"]
    )

    st.markdown('📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!')

# Store LLM-generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to generate LLM response using Hugging Face API
def generate_response(prompt_input, token, model):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    data = {"inputs": prompt_input}
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Ensure HTTP errors are handled
        generated_text = response.json()[0]['generated_text']
        return generated_text
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the model API: {e}")
        return "I'm sorry, there was an issue with the request. Please try again."
    except KeyError:
        st.error("Unexpected response format from the model API.")
        return "I'm sorry, there was an issue with the response format."

# User-provided prompt
if prompt := st.chat_input(disabled=not hf_token):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_token, model_choice)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
