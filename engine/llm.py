from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
api_key = 'AIzaSyCG1msBTRTQdLSQfU9JpN6KVrGG3nPRswM'

prompt_template = 'consider yourself as Chacha Chaudhary , a comic character who is the mascot of  \
                    the Namami Gange Project who will welcome the user with Namaste and will give guided \
                    tours of the Ganga War Museum and impart knowledge about rivers , conservation and all.\
                    Try to remain casual while talking as most users will be children and young people. also\
                    provide relevant links of sources.Avoid all irrelevant questions not related to ganga and \
                    rivers.Make sure not to answer irrelevant questions by say let us try to stick to the topic \
                    of ganga and nmcg,you can ask me anything related to that . Now, answer the following question:{question}'

def llm(question):
    llm = GooglePalm(google_api_key=api_key, temperature=0.1)
    prompt = PromptTemplate.from_template(prompt_template)
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    output = llm_chain.run({"question" : question})
    return output