from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, Literal
from util_llm import invoke, llm_with_tools, get_llm
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_tavily import TavilySearch

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

tavily_tool = TavilySearch(max_results=3)

@tool
def weather(location:str) -> str:
    '''
        provide a quick weather update for provided location
    '''
    print('weather called')
    return 'Pleasent'


tools = [weather, tavily_tool]
llm_with_tools = get_llm().bind_tools(tools)

def chat(state: AgentState)-> AgentState:
    response = llm_with_tools.invoke(state['messages'])
    return  {"messages": [response]}

graph = StateGraph(AgentState)

graph.add_node('chat', chat)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, 'chat')
graph.add_conditional_edges('chat', tools_condition);
graph.add_edge('tools', 'chat');
graph.add_edge('chat', END);
#graph.add_edge('tools', END);

app = graph.compile()
app.get_graph().print_ascii()

userAsk = input("Ask what ever you are looking for (type exit to close) ? : ")

while (userAsk.endswith("exit")== False):    
    #system_message = SystemMessage(content="You are a helpful assistant for general user asks.")
    #user_message = HumanMessage(content=userAsk)
    message = {"messages": [("user", userAsk)]}


    result = app.invoke(message)
    print('#' * 72 )
    print(result['messages'][-1].content[0]['text'])

    print('*' * 72 )
    userAsk = input("Ask what ever you are looking for (type exit to close) ? : ")

print("Agent Exit...")