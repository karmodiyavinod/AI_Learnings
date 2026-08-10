from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated, Literal
from util_llm import invoke, get_llm
from rag_util import get_retriever
from langchain_core.tools import tool
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode


class State(TypedDict):
    messages: Annotated[list, add_messages]
    query: str

@tool
def rag_query(query: str)-> str:
    '''
        RAG data loaded with a profile
        this tool is helpful to query on same data
    '''
    retriever = get_retriever('')
    rag_response = retriever.invoke(query)
    print(f'RAG Query: {query}\n\n RAG Response: {rag_response}')
    return rag_response 
    
tools = [rag_query]
llm_with_tools = get_llm().bind_tools(tools)

def query(state:State):
    query = input('Ask: ')
    if query == 'exit':
        raise ValueError("Existing...")
    
    return {"messages": [("user", query)]}
    

def get_message(state:State):
    
    #print(f'AI Query: {state["messages"]}')

    response = llm_with_tools.invoke(state['messages'])

    #print(f'AI Response: {response}')

    return  {"messages": [response]}
        
graph = StateGraph(State);
graph.add_node('query',query)
graph.add_node('get_message',get_message)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, 'query')
graph.add_edge('query','get_message')
graph.add_conditional_edges('get_message', tools_condition)
graph.add_edge('tools', 'get_message')
graph.add_edge('get_message', END)

app = graph.compile()

app.get_graph().print_ascii()

while(True):
    state = State()
    result = app.invoke(state)
    print('AI Response: ',('*' * 100))
    
    print(result['messages'][-1].text)


