from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, Literal
from util_llm import invoke, llm_with_tools, get_llm
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage

class TripPlanner(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    days: int
    destination: str
    hotel: float
    flight: float
    food: float
    total_budget: float
    activities: str
    weather: str
    best_time: str
    best_food: str
    places_to_visit: str
    
def user_input(state:TripPlanner):
    state['days'] = int(input('Provide No. of days: '))
    state['destination'] = input('Provide Destination: ')
    return state

def places_to_visit(state: TripPlanner):
    state['places_to_visit'] = 'temples, beaches'
    return state

def other_activities(state: TripPlanner):
    state['activities'] = 'horse riding '
    return state

def local_food(state: TripPlanner):
    state['best_food'] = 'Pani Puri'
    return state

def flight_budget(state: TripPlanner):
    state['flight'] = 10000
    return state

def hotel_budget(state: TripPlanner):
    state['hotel'] = 20000
    return state

def food_budget(state: TripPlanner):
    state['food'] = 15000
    return state

def summarize(state: TripPlanner):
    print('summary: ')
    print(state)
    return state

@tool
def weather(location:str) -> str:
    '''
        provide a quick weather update for provided location
    '''
    print('weather called')
    return 'Pleasent'

@tool
def total_budget(flight: float, hotel: float, food: float) -> float:
    '''
        provide total budget by sum up for flight, hotel and food
    '''
    print('total_budget called')
    return flight + hotel + food

tools = [weather, total_budget]
llm_with_tools = get_llm().bind_tools(tools)

graph = StateGraph(TripPlanner)

graph.add_node('user_input', user_input)
graph.add_node("tools", ToolNode(tools))
graph.add_node('places_to_visit', places_to_visit)
graph.add_node('other_activities', other_activities)
graph.add_node('local_food', local_food)
graph.add_node('hotel_budget', hotel_budget)
graph.add_node('flight_budget', flight_budget)
graph.add_node('food_budget', food_budget)
graph.add_node('total_budget', total_budget)
graph.add_node('summarize', summarize)

graph.add_edge(START, 'user_input')
graph.add_edge('user_input', 'places_to_visit');

#graph.add_edge('user_input', 'places_to_visit')

graph.add_edge('places_to_visit', 'other_activities')
graph.add_edge('other_activities', 'local_food')
graph.add_edge('local_food', 'flight_budget')
graph.add_edge('flight_budget', 'hotel_budget')
graph.add_edge('food_budget', 'food_budget')
graph.add_edge('food_budget','summarize')
#graph.add_edge('other_activities','summarize')
#graph.add_edge('local_food','summarize')

#graph.add_edge('flight_budget', 'total_budget')
#graph.add_edge('hotel_budget','total_budget')
#graph.add_edge('food_budget','total_budget')

#graph.add_edge('total_budget', 'summarize')


graph.add_conditional_edges('summarize', tools_condition);
graph.add_edge('tools', 'summarize');

#graph.add_edge('summarize', END)

app = graph.compile()
app.get_graph().print_ascii()

state = { 'messages': 
         [("system",'You are a trip planner assistent, please plan a user trip based provide input as no of days and destination'
'you want to check weather of destination and sum of total bduget too and summarize overall plan in bullet points'), 
("user","plan my trip as per input provied")]}

result = app.invoke(state)
print('#' * 72 )
print(result)