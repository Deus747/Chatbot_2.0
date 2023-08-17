import streamlit as st
from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

def download_chat_history():
    conversation_memory = st.session_state.conversation.memory.buffer
    #content = '\n'.join(conversation_memory)  # Assuming each line of the conversation is a string
    data = conversation_memory.encode('utf-8')  # Encode the content as bytes

    st.sidebar.download_button(
        label="Download Chat History",
        data=data,
        file_name="history.txt",
        mime="text/plain",  # Set the MIME type to indicate it's a text file
    )




st.title("Chatbot")



if "conversation" not in st.session_state:
    llm = OpenAI(
    temperature=0.2,
    openai_api_key=st.secrets["openai_api_key"],
    model_name="text-davinci-003"
    )
    memory = ConversationBufferMemory()
    st.session_state.conversation = ConversationChain(
    llm=llm,
    memory=memory,
    )

if "messages" not in st.session_state:
    st.session_state.messages = []
    



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        full_response = st.session_state.conversation.run(
            prompt
        )
        st.markdown(full_response)          
    st.session_state.messages.append({"role": "assistant", "content": full_response})




download_chat_history()
    
