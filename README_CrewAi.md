# Crew AI

### Core Components 
  * **Agent** - An Agent is an autonomous AI worker designed to play a specific role within a team, much like a human professional.
    * LLM - Model
    * Role: Defines the agent's job title or specialty (e.g., "Senior Research Analyst", "Content Writer").
    * Goal The objective or target the agent is trying to accomplish.
    * Backstory: Narrative context that guides the agent's behavior, tone, and decision-making persona.
    * Memory: Capabilities enabling agents to remember past interactions and delegate tasks to other agents when necessary
    * Tool: Specific functions or utilities the agent can use to complete its work.

  * **Tasks** - A job, A actionable component, manager all agants, tools to achive goal
    * Description: Clear, actionable instructions detailing what needs to be done.  
    * Expected Output: A precise definition of what the final result should look like (e.g., a markdown report, a JSON object, or a Pydantic model).  
    * Agent: The specific team member responsible for executing the task.  Context & Async Execution: Parameters allowing tasks to use outputs from previous tasks as context or run asynchronously.

  * **Tools** - ToolsTools are skills or external utilities that agents can use to interact with the world, process data, or execute code.        
    * Built-in Tools: Ready-to-use utilities provided by CrewAI (such as web scrapers, search engines, and file readers via crewai_tools).  
    * Custom Tools: User-defined functions tailored for specific APIs, databases, or proprietary systems.  
    * Integrations: Compatibility with LangChain tools and support for standard protocols like Model Context Protocol (MCP).


  * **Process** - ProcessesA Process defines the execution workflow or project management strategy that guides how tasks are distributed and handled by the agents:  
    * Sequential Process: Executes tasks one after another in a linear order.  
    * Hierarchical Process: Introduces a manager agent (or a designated LLM) that delegates tasks, reviews outputs, and validates results before final completion.

  * **Crew AI Crews (Intelligance)** - A Crew is the overarching collaborative unit that brings together agents, tasks, processes, and tools into a single operational team.  It orchestrates how the agents work together toward a shared high-level objective.  Manages shared short-term/long-term memory, caching mechanisms to speed up tool execution, and performance tracking/metrics.  Initiated using execution methods like kickoff().

  * **Crew AI Flows (Backbone)** - Flows allow developers to build complex, multi-stage, event-driven pipelines above standard crews.  Enable state management across multiple steps.  Provide programmatic control (conditional branching, loops, and triggers) to chain multiple crews and external logic together.

  
### Platforms
 
 * **CrewAI Enterprise /AMP**
 * **CrewAI** Open Source
 * **CrewAI Studio UI** 

### Development Mode
 * Crew Studio
 * CLI
 * YAML Configuation
 * Crew Package
 
  


 

  
