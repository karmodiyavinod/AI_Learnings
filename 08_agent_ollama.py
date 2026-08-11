from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama

class State(TypedDict):
    messages: Annotated[list, add_messages]

cnf = {"configurable": {"thread_id": "session-123"}}    

prompt = ChatPromptTemplate.from_messages([
    ("system", 
            '''You are a helpful assistent for a simple text summarization'''),
    MessagesPlaceholder(variable_name="messages")
])

def llm_ollama():
    return ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

chain = prompt | llm_ollama()

def ask(state:State):
    query = input('Ask: ')
    return {"messages": [("user", query)]}

def llm_call(state:State):
    response = chain.invoke(state['messages'])
    return  {"messages": [response]}

# nodes    
graph = StateGraph(State);
graph.add_node('ask',ask)
graph.add_node('llm_call',llm_call)

#edges
graph.add_edge(START, 'ask')
graph.add_edge('ask','llm_call')
graph.add_edge('llm_call', END)
# graph

app = graph.compile(checkpointer=MemorySaver())
app.get_graph().print_ascii()

message = { }
result = app.invoke(message, config=cnf)

print(result['messages'][-1].content)