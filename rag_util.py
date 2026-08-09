#from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_unstructured.document_loaders import UnstructuredLoader
from langchain_core.documents import Document  # Correct location
from enum import Enum
from env_service import get_gemini_api_key, get_gemini_embedding_model
import time
import os
persist_directory = "./chroma_unstructured_db"
chunk_size:int = 50
chunk_overlap:int = 12
embeddings = GoogleGenerativeAIEmbeddings( model=get_gemini_embedding_model(), 
                                           api_key=get_gemini_api_key(),
                                           max_retries=6)

class Doc_File_Type(Enum):
    PDF = 1
    EXCEL = 2
    JSON = 3

def get_docs(path: str, type: Doc_File_Type)->list:
    loader = UnstructuredLoader(
        file_path=path,
        strategy="fast",
        #strategy="hi_res",             # "hi_res", "fast", or "ocr_only"
        partition_via_api=False,       # Set True if using Unstructured API key
        mode="elements"                # "elements" returns individual document blocks (tables, headers, narrative text)
    )

    docs = loader.load()

    return docs

def get_chunks(docs: list)->list:
 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    return text_splitter.split_documents(docs)


def get_chunks_from_text(text: str)->list:
 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    return text_splitter.split_text(text)
    
def get_retriever(contents: str):
    
    vector_store = Chroma(
        embedding_function=embeddings,  # Fixed argument name
        collection_name="unstructured_pdf_collection",
        persist_directory=persist_directory
    )

    if os.path.exists(persist_directory) == False:
        chunks = get_chunks_from_text(' '.join(contents))
        vector_store.add_texts(chunks)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}  # Retrieve the top 2 most relevant chunks
    )

    return retriever
    
def test_rag_query(query):
    #doc_data = get_docs('docs\profile.pdf', Doc_File_Type.PDF) 
    
    doc_data = [
        'Vinod Karmodiya, 19 years of expertise in architecting, engineering, and delivering high-performance enterprise solutions',
        'Certified in Microsoft AI Fundamentals, the profile seamlessly bridges robust legacy modernization with cutting-edge innovations, specializing in .NET technologies, Angular, TypeScript, Microservices architectures, RESTful APIs, Elasticsearch cache optimization, and automated ASPOSE document engineering',
        'A pioneer in next-generation intelligence, expertise extends to implementing Generative AI frameworks, Python LangGraph Agentic workflows, Retrieval-Augmented Generation (RAG) architectures, and LangSmith observability across OpenShift container platforms. Recognized for strategic technical governance and end-to-end delivery management, the leader excels at steering cross-functional teams, optimizing system performance, and driving organizational success through scalable, mission-critical solution design'
    ]

    retriever = get_retriever(doc_data)

    results = retriever.invoke(query, k=3)

    print('*'*100)
    print(results)
    print('*'*100)

# test_rag_query('who is Vinod Karmodiya')
test_rag_query('which type of certs he has')
