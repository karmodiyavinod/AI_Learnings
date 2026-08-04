from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from util_llm import invoke

class State(TypedDict):
    name: str
    message: str
    ai_message: str

def userInput(state:State):
    state['name'] = input('Enter Your Name: ')
    return state

def getMessage(state:State):
    state['ai_message'] = invoke(f"Prepare a gratitude message for new user named {state['name']} in just single line.")
    return state

def composeMessage(state:State):
    state['message'] = f'{state['name']} =>  {state['ai_message']}'
    return state

graph = StateGraph(State);
graph.add_node(userInput)
graph.add_node(getMessage)
graph.add_node(composeMessage)

graph.add_edge(START, 'userInput')
graph.add_edge('userInput', 'getMessage')
graph.add_edge('getMessage', 'composeMessage')
graph.add_edge('composeMessage', END)


app = graph.compile()

app.get_graph().print_ascii()

state = State()
result = app.invoke(state)

print(result['message'])


