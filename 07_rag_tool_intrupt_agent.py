from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated
from util_llm import get_llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

class State(TypedDict):
    messages: Annotated[list, add_messages]
    approved: bool
    draft: str

cnf = {"configurable": {"thread_id": "session-123"}}    

prompt = ChatPromptTemplate.from_messages([
    ("system", 
            '''You are a helpful python code builder assistant powered by Google Gemini.
                Please generate pure code, no comment and explaintion is required.'''),
    MessagesPlaceholder(variable_name="messages")
])

chain = prompt | get_llm()

def is_approved(message: str):
    return str(message).strip().lower() in ("approve","approved","yes"," go ahead","good")    

def query(state:State, config: RunnableConfig):
    query = input('Ask: ')
    if query == 'exit':
        raise ValueError("Existing...")
    
    return {"messages": [("user", query)]}

def code_develop(state:State, config: RunnableConfig):
    response = chain.invoke(state['messages'])
    return  {"messages": [response]}

def human_review(state:State, config: RunnableConfig):
    code_generated = state['messages'][-1].text
    print('START Code to review'+ '*' * 50)
    print(code_generated)
    print('END review'+ '*' * 50)
    
    decision = interrupt({'draft': 'Instructions: Reply "Approve" to approve or provide review commnent!!'})

    if(is_approved(decision)):
        return { 'approved': True, "messages": [AIMessage("APPROVED")]}

    return { 'approved': False, "messages": [HumanMessage(f"Revise it: {decision}")]}

def route_post_review(state: State, config: RunnableConfig):
    return 'end' if state.get('approved') else 'code_develop'    

# nodes    
graph = StateGraph(State);
graph.add_node('query',query)
graph.add_node('code_develop',code_develop)
graph.add_node('human_review',human_review)
graph.add_node('route_post_review',code_develop)

#edges
graph.add_edge(START, 'query')
graph.add_edge('query','code_develop')
graph.add_edge('code_develop','human_review')
graph.add_conditional_edges('human_review', route_post_review, { 'end': END, 'code_develop': 'code_develop'})

# graph

app = graph.compile(checkpointer=MemorySaver())
app.get_graph().print_ascii()


#while(True):
state = State()
message = { 'approved': False}
result = app.invoke(message, config=cnf)

while(True):
    pause = result['__interrupt__'][0].value
    print(f'PAUSED: {pause}')

    user_approval = input('Please approve or provide review comment": ')

    final = app.invoke(Command(resume=user_approval, update=state), config=cnf)

    approval_messgae = final['messages'][-1].text;

    if(is_approved(approval_messgae)):
        print('Final after review: ',('*' * 100))
        print(approval_messgae)
        break
    else:
        print('Revise: ',('*' * 100))
        Command(update='', goto='human_review') 

