# AI_ML_Projects
Project created during learnings this tech stack

Display Graph:
  # display(Image(app.get_graph().draw_mermaid_png()))
  # app.get_graph().print_ascii()

# Each branch as a leaned project created as POC during learning the tech stack
  1. 01_basic -  Basic Lang Graph Agent
  2. 02_conditional_agent - Conditional Lang Graph Agent
  3. 03_tools_agent - Tool Lang Graph Agent
  4. 04_memory_agent - agentic with memory 
  5. 05_rag_agent - with simple RAG use
  6. 06_rag_tool_agent - agetic rag
  7. 07_rag_tool_intrupt_agent - agentic rag with tool and intruption as human in loop
  8. 08_agent_ollama - simple ollama local llm use
  
# Gemini Models:
1. gemini-3.1-flash-lite
2. gemini-3.6-flash

# Setup Ollama for local llms
1. download for windows: https://ollama.com/download/windows
2. install llama model: ollama run llama3.2:3b (requires min ~2 GB RAM)
3. use in yuor lang graph agent: 
    install package: pip install -U langchain-ollama
    ChatOllama(model="llama3.2:3b", temperature=0.5)

