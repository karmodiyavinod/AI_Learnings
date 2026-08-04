from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal

class State(TypedDict):
    name: str
    message: str

def userInput(state:State):
    state['name'] = input('Enter Your Name: ')
    return state

def composeMessage(state:State):
    state['message'] = f'Hello {state['name']}'
    return state

graph = StateGraph(State);
graph.add_node(userInput)
graph.add_node(composeMessage)

graph.add_edge(START, 'userInput')
graph.add_edge('userInput', 'composeMessage')
graph.add_edge('composeMessage', END)


def startAgent():

    app = graph.compile()

    app.get_graph().print_ascii()

    state = State()
    result = app.invoke(state)
    print(result['message'])
    return result


