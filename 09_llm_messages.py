from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from util_llm import get_llm, llm_ollama

system_message = [SystemMessage('''You are an AI Technology Expert. Answer in crips and clearner manner just 20 words.''')]

print(' *' * 20)
print('System Message:')
print(' *' * 20)
print(system_message)

chain = llm_ollama() #get_llm()  #llm_ollama()

def call():
    human_message = [HumanMessage("What is RAG?")]

    print(' *' * 20)
    print('Human Message:')
    print(' *' * 20)
    print(human_message)
    
    input_messages = system_message + human_message
    
    print(' *' * 20)
    print('input Message:')
    print(' *' * 20)
    print(input_messages)

    ai_response =  chain.invoke(input_messages)

    print(' *' * 20)
    print('AI Reponse Message:')
    print(' *' * 20)
    print(ai_response)

call()
