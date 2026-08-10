from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated
from util_llm import get_llm
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
class State(TypedDict):
    messages: Annotated[list, add_messages]
    approved: bool
    draft: str
    
prompt = ChatPromptTemplate.from_messages([
    ("system", 
            '''You are a helpful python code builder assistant powered by Google Gemini.
                Please generate pure code, no comment and explaintion is required.'''),
    MessagesPlaceholder(variable_name="messages")
])

chain = prompt | get_llm()

def query(state:State):
    query = input('Ask: ')
    if query == 'exit':
        raise ValueError("Existing...")
    
    return {"messages": [("user", query)]}

def code_develop(state:State):
    print('code_develop.')
    print(state['messages'])

    response = chain.invoke(state['messages'])
    return  {"messages": [response]}

def human_review(state:State):
    code_generated = state['messages'][-1].text
    print('START Code to review'+ '*' * 50)
    print(code_generated)
    print('END review'+ '*' * 50)

    decision = interrupt({'draft': 'Instructions: Reply "Approve" to approve or provide review commnent!!'})

    print(f'human_review: {decision}')
    if(str(decision).strip().lower() in ("approve","approved","yes"," go ahead","good")):
        print('Approved')
        return { 'approved': True, "messages": [AIMessage("APPROVED")]}


    return { 'approved': False, "messages": [HumanMessage(f"Revise it: {decision}")]}

def route_post_review(state: State):
    print(f'route_post_review: {result['messages'][-1].text}')

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
cnf = {"configurable": {"thread_id": "session-123"}}

app = graph.compile(checkpointer=MemorySaver())
app.get_graph().print_ascii()

#while(True):
state = State()
message = { 'approved': False}
result = app.invoke(message, config=cnf)


pause = result['__interrupt__'][0].value
print(f'PAUSED: {pause}')

user_approval = input('approved or comment..')

print('Human Review >>')
final = app.invoke(Command(resume=user_approval), config=cnf)

print('Final after review: ',('*' * 100))
print(final['messages'][-1].text)


