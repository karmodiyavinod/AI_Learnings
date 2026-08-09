from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from util_llm import invoke
from rag_util import get_retriever

class State(TypedDict):
    query: str
    rag_message: list
    message: str
    ai_message: str

def query(state:State):
    state['query'] = input('Ask: ')
    return state

def rag_query(state: State):
    
    doc_data = [
        'Vinod Karmodiya, 19 years of expertise in architecting, engineering, and delivering high-performance enterprise solutions',
        'Certified in Microsoft AI Fundamentals, the profile seamlessly bridges robust legacy modernization with cutting-edge innovations, specializing in .NET technologies, Angular, TypeScript, Microservices architectures, RESTful APIs, Elasticsearch cache optimization, and automated ASPOSE document engineering',
        'A pioneer in next-generation intelligence, expertise extends to implementing Generative AI frameworks, Python LangGraph Agentic workflows, Retrieval-Augmented Generation (RAG) architectures, and LangSmith observability across OpenShift container platforms. Recognized for strategic technical governance and end-to-end delivery management, the leader excels at steering cross-functional teams, optimizing system performance, and driving organizational success through scalable, mission-critical solution design'
    ]

    retriever = get_retriever(doc_data)
    state['rag_message'] = retriever.invoke(state['query'])
    return state

def get_message(state:State):
    state['ai_message'] = invoke(f"format question: {state['query']}, and its response: {state['rag_message']}.")
    return state

graph = StateGraph(State);
graph.add_node(query)
graph.add_node(get_message)
graph.add_node(rag_query)

graph.add_edge(START, 'query')
graph.add_edge('query', 'rag_query')
graph.add_edge('rag_query', 'get_message')
graph.add_edge('get_message', END)

app = graph.compile()

app.get_graph().print_ascii()

state = State()
result = app.invoke(state)

print(result['ai_message'].text)


