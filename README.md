# Business Idea Generator: In build autonomous AI Agents to generate ideas
Agentic AI Application that helps generating ideas of your choice.

![Autonomous Agent](assets/Agentic-AI.gif)

## Overview
A Flask-based REST API that generates creative business ideas using AutoGen AI agents. The API leverages multiple AI agents with different specialties to create, refine, and iterate on business concepts.
### Features
- **Multi-Agent AI System:**  Uses AutoGen framework with specialized agents
- **RESTful API:** Clean, well-documented API endpoints
- **Areas of interest:** Focus on business domains you're passionate about or exploring.
- Designed to spark **creativity, collaboration, and customization**.

<!-- ## Before you begin

I'm here to support your success in any way I can! If you ever have questions, need guidance, or just want to say hello, feel free to reach out — whether through the platform or directly via email at senapatibipul9@gmail.com.
I also love connecting with fellow developers, creators, and curious minds on LinkedIn.
🌐 https://linkedin.com/in/senapatibipul  -->

## Table of Contents

- [Installation](#Installation)
  - [Clone the Repository](#Clone-the-repository)
  - [Create & Activate Virtual Environment](#Create-&-Activate-the-virtual-environment)
  - [Environment Variables](#environment-variables)
  - [Install Dependencies](#install-dependencies)
  - [Run the Application](#Run-the-Application)
- [API Documentation](#API-Documentation)
    - [Endpoints](#Endpoints)
- [Output Expectations](#Output-Expectations)
    - [Steps & Sample video execution](#Output-Expectations)
- [Project Structure](#project-structure)
- [Pre-requisites on LLM](#Pre-requisites-on-LLM)

## Installation

1. Clone the Repository:
```
    git clone https://github.com/bipulsenapati998/investing-agent.git
    cd src
```
2. Create & Activate the virtual environment:
```
    Use venv	python -m venv llms && source llms/bin/activate
    Use conda	conda create -n llms python=3.10 && conda activate llms  
```
3. Update the .env file with your OpenAI API key:
```
    OPENAI_API_KEY=<your_actual_api_key_here>
```
4. Install Dependencies:
```
    pip install -r requirement.txt
```
5. Run the Application:
```
   uv run app.py // Direct Approach

   uv run flask_api.py // Consumable endpoint
```
## API Documentation
### Base URL
```
http://localhost:50051
```

### Endpoints
#### Health Check:
```
GET /health
```
#### Response:
```
{
    "host": "localhost",
    "model": "gpt-4o-mini",
    "no_of_agents": 5,
    "port": 50051,
    "status": "healthy",
    "temperature": 1.0,
    "timestamp": "2025-07-11T05:06:03.011439",
    "version": "1.0",
    "expcted_no_of_ideas": 5
}
```
#### Generate Business Ideas
```
POST /api/v1/ideas
Content-Type: application/json

{
    "num_ideas": 3
}
```
#### Response:
```
{
    "message": "Ideas generated successfully on path:src/idea"
}
```
## Output Expectations
```
> Checkout Sample ideas on "src/ideas" folder from five distinct Worker agent.

> Checkout autonomus agent discussions on "src/agents" folder.

> Consult to flow diagram in the assets folder for comprehensive understanding on Agentic AI.
```
![Output Execution flow](assets/business_idea_generator_agentic_ai.gif)
## Project Structure
```
assets
|    |── Agentic-AI.gif         # Design Diagram
|    |── output Image.png       # Sample output
src
|    ├── config/                # Configuration files
|    │   ├── load_config.py     # Configuration loader
|    │   └── logger_config.py   # Logging configuration
|    ├── scripts/               # Deployment scripts
|    │   ├── setup_env.sh       # Environment setup
|    │   ├── run_tests.sh       # Test runner
|    │   └── deploy.sh          # Deployment script
|    ├── logs/                  # Log files
|    ├── agent/agent1,agent2..  # Generated agent files
|    ├── idea/idea1,idea2...    # Generated idea files
|    ├── agent.py               # Agent implementation
|    ├── creator.py             # Creator agent
|    ├── messages.py            # Message utilities
|    ├── flask_api.py           # Endpoints
requirements.txt                # Python dependencies
README.md                       # This file
config.json                     # Global Config
.env                            # Secrets

```
## Pre-requisites on LLM
- OpenAI (Recommended)
The default model used is "gpt-4o-mini", provided by OpenAI.
To use it, you'll need to obtain your API key and set up billing via:

-  OpenAI Billing Settings:https://platform.openai.com/settings/organization/billing/

 Alternative Models
You can also experiment with other cutting-edge LLMs:

    Claude: claude-3-7-sonnet-latest

    Gemini: gemini-2.0-flash

    DeepSeek: deepseek-chat

These models may offer different strengths depending on your use case.

> Local & Cost-Effective Option (Ollama)
For a completely free and local alternative, use Ollama with models like llama3.2.

Here's a quick setup snippet:
```
from openai import OpenAI

ollama = OpenAI(base_url='http://localhost:11444/v1', api_key='ollama')
model_name = "llama3.2"

response = ollama.chat.completions.create(model=model_name, messages=messages)
```