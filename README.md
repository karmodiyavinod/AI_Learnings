
## Setup

### Install UV Tool

uv tool list

uv tool uninstall crewai`

Example: uv tool install crewai==1.14.4

uv tool list

1. Install node uv tool list

2. Run this command:  

npx skills add crewaiinc/skills

**Note** - Please install githu cli and process below step in case above command giving auth exception
 * gh auth login
 * npx skills add crewaiinc/skills OR npx skills add git@github.com:crewaiinc/skills.git
 * Choose options

CrewAI docs => https://docs.crewai.com/en/introduction

**python** python version
    uv python pin 3.13
    uv venv --python 3.13
    .venv\Scripts\activate
    or  source .venv/scripts/activate

    Upgarde relevant tool if require
    like: uv pip install --upgrade chromadb crewai

