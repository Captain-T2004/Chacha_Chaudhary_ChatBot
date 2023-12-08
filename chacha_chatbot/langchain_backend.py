from langchain.document_loaders import WebBaseLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.llms import GooglePalm
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()
import os


llm = GooglePalm(google_api_key=os.environ['GOOGLE_API_KEY'], temperature=0.1)



instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
vector_db_path = "fiass_index"

def create_vector_db():
    loader = WebBaseLoader(["https://nmcg.nic.in/about_nmcg.aspx", "https://nmcg.nic.in/","https://nmcg.nic.in/whos_who.aspx","https://nmcg.nic.in/CleanGangaFund/AboutCGF.html"])

    data = loader.load()
    vectordb = FAISS.from_documents(documents=data,
                                 embedding=instructor_embeddings)
    
    
    vectordb.save_local(vector_db_path)


def get_answer_chain():
    # Load the vector database from the local folder
    vectordb = FAISS.load_local(vector_db_path, instructor_embeddings)

    # Create a retriever for querying the vector database
    retriever = vectordb.as_retriever(score_threshold=0.7)

    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type="stuff",
                                        retriever=retriever,
                                        input_key="query",
                                        return_source_documents=True,
                                        chain_type_kwargs={"prompt": PROMPT})

    return chain



if __name__ == "__main__":
#    create_vector_db()
    chain = get_answer_chain()
    while True:
        question = input("Ask a question: ")
        answer = chain(question)
        print(answer)


