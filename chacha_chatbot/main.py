import streamlit as st
from langchain_backend import get_answer_chain, create_vector_db

st.title("ChaCha Chadhary Chatbot")
image_path = "download.png"
image = st.image(image_path, caption="Chacha Chaudhary", use_column_width=True)
btn = st.button("Get Latest Data")
if btn:
    create_vector_db()

question = st.text_input("Question: ")

if question:
    chain = get_answer_chain()
    response = chain(question)

    st.header("Answer")
    st.write(response["result"])
    


