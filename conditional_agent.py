from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Literal
from util_llm import invoke

class AgentState(TypedDict):
    message: str
    ai_message: str
    department: str

def intialMessage(state:AgentState):
    state['message'] = input('Provide your work profile')
    return state

def getMessage(state:AgentState):
    state['ai_message'] = invoke(f'''
        Categorize deparment based on work profile,
         - Work Profile is: {state['message']}
         - Expected deparments are it_department, billing_department, hr_department, unknow_department
        Provide specific department only as repsonse
    ''')
    print(state)
    return state

def route(state:AgentState):
    return state['ai_message']

def it_department(state:AgentState):
    state['department'] = 'it_department'
    return state

def billing_department(state:AgentState):
    state['department'] = 'billing_department'
    return state

def hr_department(state:AgentState):
    state['department'] = 'hr_department'
    return state

def unknow_department(state:AgentState):
    state['department'] = 'unknow_department'
    return state

graph = StateGraph(AgentState);
graph.add_node(intialMessage)
graph.add_node(getMessage)
graph.add_node(it_department)
graph.add_node(billing_department)
graph.add_node(hr_department)
graph.add_node(unknow_department)

graph.add_edge(START, 'intialMessage')
graph.add_edge('intialMessage', 'getMessage')
graph.add_conditional_edges("getMessage", route, 
                            {
                                'it_department':'it_department',
                                'billing_department':'billing_department',
                                'hr_department':'hr_department',
                                'unknow_department':'unknow_department'
                            })


graph.add_edge('it_department', END)
graph.add_edge('billing_department', END)
graph.add_edge('hr_department', END)
graph.add_edge('unknow_department', END)

app = graph.compile()

app.get_graph().print_ascii()

state = AgentState()
result = app.invoke(state)

print('#' * 5 )
print(result)


