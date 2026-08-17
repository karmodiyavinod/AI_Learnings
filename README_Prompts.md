
# Prompt Engineering - A quick understading 

#### Prompt engineering is the practice of structuring, refining, and optimizing inputs (prompts) to guide Large Language Models (LLMs) toward generating the most accurate, creative, and contextually relevant outputs.

### Techniques
* Core Prompting Techniques
  * **Zero-Shot Prompting**  Instructing the model to perform a task without providing any prior examples. It relies entirely on the model's pre-trained knowledge. Straightforward tasks like summarization, translation, or general classification.  
  * **Few-Shot Prompting**  Providing a small number of input-output examples inside the prompt to guide the model toward the expected format, tone, or style. Complex formatting tasks, specific stylistic requirements, or unique classification boundaries.

* Advanced Reasoning Techniques
  * **Chain-of-Thought (CoT) Prompting** Forcing the model to break down a complex problem into smaller, logical intermediate steps rather than jumping straight to an answer. Multi-step math problems, logic puzzles, or code debugging.  
  Example: "A store has 10 apples. They sell 4, and then buy 12 more. How many apples do they have? Think step by step."
  * **Self-Consistency** Generating multiple independent reasoning paths (rollouts) for the same prompt and choosing the most commonly agreed-upon final answer. Mitigating the risk of random reasoning errors in math or logic tasks.
  * **Tree-of-Thoughts (ToT)** Generalizing Chain-of-Thought by allowing the model to explore multiple reasoning branches at each step, evaluate them, and self-correct or backtrack (resembling a tree search). Strategic planning, creative writing, or complex problem-solving with multiple pathways.

* Tree-of-Thoughts (ToT)
  * **Role-Prompting (Persona Pattern)** Assigning a specific identity, profession, or perspective to the LLM. When you need output tailored to a specific audience, domain expertise, or tone. 
  Example: "Act as a senior cybersecurity auditor and review the following network architecture for vulnerabilities."
  * **Generated Knowledge Prompting** Prompting the model to first generate relevant background facts or knowledge about a topic before using that generated context to answer the primary prompt.
  * **Least-to-Most Prompting** Decomposing a complex problem into a sequence of progressively harder sub-problems, solving them sequentially where each step builds on the previous answer. Highly complex workflows that overwhelm standard single-pass reasoning.

* Agentic & Iterative Frameworks
  * **ReAct (Reasoning + Acting)** Interleaving verbal reasoning traces with external actions (such as searching the web, running code, or querying databases). AI agents that need to fetch real-time data or interact with software environments.
  * **Meta-Prompting** Using the LLM to write, critique, or optimize prompts for itself or other models. Automated prompt optimization pipelines.

