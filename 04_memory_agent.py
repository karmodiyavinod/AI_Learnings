from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated, Literal
from util_llm import invoke, llm_with_tools, get_llm
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
# short term memmory and thread checkpointing 

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

llm = get_llm()

def chat(state: AgentState)-> AgentState:
    response = llm.invoke(state['messages'])
    return  {"messages": [response]}

graph = StateGraph(AgentState)

graph.add_node('chat', chat)

graph.add_edge(START, 'chat')
graph.add_edge('chat', END);

app = graph.compile(checkpointer=MemorySaver())
app.get_graph().print_ascii()

def _text(msg):
    '''Sometime Gememi returning in content block'''

    c=msg.content

    if isinstance(c, str):
        return c

    return "".join(p.get("text","") for p in c if isinstance(p, dict))

def say(thread_id, text):
    print(thread_id)
    print(text)
    
    config = {"configurable": {"thread_id": thread_id}}
    message = {"messages": [SystemMessage("Keep your answer in short to optimized use of token"), HumanMessage(text)]}

    result = app.invoke(message, config=config)

    print(f'You: {text}')
    print(f'[thread: {thread_id}] >> bot: {_text(result['messages'][-1])}');

thread: int = 1
userAsk = input(f"[thread: 'thread_'{str(thread)}] >>Ask what ever you are looking for (type exit to close) ? : ")
while (userAsk.endswith("exit")== False):    

    print('#' * 72 )

    print(say('thread_'+str(thread), userAsk))
    if thread == 2:
        thread = 1
    else:
        thread = 2

    print('*' * 72 )

    userAsk = input(f"[thread: 'thread_'{str(thread)}] >>Ask what ever you are looking for (type exit to close) ? : ")

print("Agent Exit...")