import os



from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_openai import ChatOpenAI
from langchain_community.llms import CTransformers


# from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

embedding = OpenAIEmbeddings()
persist_directory = 'db'

turbo_llm = ChatOpenAI(
    temperature=0,
    model_name='gpt-3.5-turbo'
)
def load_pdf(data):
    loader = DirectoryLoader(data,
                    glob="*.pdf",
                    loader_cls=PyPDFLoader)
    
    documents = loader.load()

    return documents

def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text)
    # Lowercase
    tokens = [token.lower() for token in tokens]
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    
    return ' '.join(tokens)


def text_splitter(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    return  texts


def create_db_vectorstore(texts,persist_directory,embedding):
    
    vectordb = Chroma.from_documents(documents=texts,
                                 embedding=embedding,
                                 persist_directory=persist_directory)
    vectordb.persist()
    vectordb = None
    return vectordb
    
def get_db_vectorstore(embedding,persist_directory):
    vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embedding)
    return vectordb

def make_retrevials(vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 2})
    return retriever


def get_chain_type_kwargs():
        prompt_template=""""
        Litigat8, designed by Faran for his final year project, offers tailored advice on UK household and tenant law, using the most up-to-date information available up to its last training cut-off in April 2023 or from real-time legal resources where accessible. This service aims to provide relevant, accurate, and user-friendly legal advice while maintaining the utmost privacy and confidentiality for its users.

        Context: {context}
        Question: {question}

        Guidelines for response by Litigat8:
        1. **User-Friendly Language:**
        - Communicate legal advice in clear, straightforward language, making complex legal principles accessible to those without a legal background.

        2. **Feedback Mechanism:**
        - Encourage feedback on the advice's usefulness and understandability, using this input to enhance Litigat8's future interactions.

        3. **Privacy Considerations:**
        - Avoid unnecessary collection of personal information, ensuring users' privacy and confidentiality in providing generalized legal guidance.

        4. **Update Mechanism:**
        - Regularly refresh Litigat8's knowledge with the latest case law, legislation, or changes in UK household and tenant law to maintain the accuracy of its advice.

        5. **Limit Scope Wisely:**
        - Focus Litigat8's advice within the realm of UK household and tenant law, avoiding areas outside its expertise or current knowledge.

        **Detailed Instructions for Litigat8:**
        - **For UK household and tenant law queries:**
        - Utilize current UK legislation and case law to form detailed advice, addressing legal ambiguities and guiding users towards professional advice when necessary.

        - **For questions about "Faran" or "Litigat8":**
        - For "Faran": Respond with, "Faran is my maker."
        - For "Litigat8": Share that it is an AI designed for providing legal advice on UK household and tenant law as a final year project by Faran.

        - **For out-of-scope inquiries:**
        - Inform users when their questions fall outside Litigat8's domain or geographic focus, recommending professional legal consultation.

        **Handling Ambiguities and Uncertainty:**
        - Clearly explain when legal issues are ambiguous and suggest seeking further advice for complex matters.

        **Communicating with Users:**
        - If needed, ask for clarification to offer more precise advice, always respecting user privacy and focusing on enhancing understanding.

        **Feedback and Continuous Improvement:**
        - Include a feedback option for users to rate the helpfulness of advice and suggest improvements, aiding in the ongoing development of Litigat8.

        Helpful answer:
        """


        PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain_type_kwargs={"prompt": PROMPT}
        return chain_type_kwargs

def make_chain(turbo_llm,retriever,chain_type_kwargs):
    qa_chain = RetrievalQA.from_chain_type(llm=turbo_llm,
                                    chain_type="stuff",
                                    retriever=retriever,
                                    return_source_documents=True,
                                    chain_type_kwargs=chain_type_kwargs)
    return qa_chain


def get_response(user_input):
    result=qa_chain({"query": user_input})
    return result["result"]


vectordb = get_db_vectorstore(embedding,persist_directory)
retriver = make_retrevials(vectordb)
chain_type_kwargs = get_chain_type_kwargs()
qa_chain = make_chain(turbo_llm,retriver,chain_type_kwargs)
    
    

    
