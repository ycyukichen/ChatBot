import streamlit as st
from ctransformers import AutoModelForCausalLM

# Set page title
st.set_page_config(page_title="🤗💬 Let's Chat")

# Sidebar information
with st.sidebar:
    st.title("🤗💬 Chat with LLaMA 2")
    st.markdown("Running LLaMA 2 locally with GGML model.")
    
# Store LLM-generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to generate responses using LLaMA 2 GGML model
def generate_response(prompt_input):
    # Load the LLaMA 2 model from the local .bin file
    model = AutoModelForCausalLM.from_pretrained(
        ".",
        model_file="llama-2-7b-chat.ggmlv3.q8_0.bin",  
        model_type="llama"  
    )

    # Generate a response
    response = model(prompt_input, max_new_tokens=50)
    return response

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)