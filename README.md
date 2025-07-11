# Business Idea Generator: In build autonomous AI Agents to generate ideas
Agentic AI Application that helps generating ideas of your choice.

![Autonomous Agent](assets/Agentic-AI.gif)

## Overview
- Designed to spark creativity, collaboration, and customization.
- You have the flexibility to customize the experience by selecting:
    > Multi-agent architecture – Choose from different intelligent agents to collaborate on idea generation.

    > Areas of interest – Focus on domains you're passionate about or exploring.
    
    > LLM of your choice

<!-- ## Before you begin

I'm here to support your success in any way I can! If you ever have questions, need guidance, or just want to say hello, feel free to reach out — whether through the platform or directly via email at senapatibipul9@gmail.com.
I also love connecting with fellow developers, creators, and curious minds on LinkedIn.
🌐 https://linkedin.com/in/senapatibipul  -->


## Installation

1. Clone the repository:
```
    git clone https://github.com/bipulsenapati998/investing-agent.git
    cd src
```
2. Activate the virtual environment:
 
     Create a virtual env of your choice and install dependencies:
```
   
    Use venv	python -m venv llms && source llms/bin/activate
    Use conda	conda create -n llms python=3.10 && conda activate llms

    pip install -r requirement.txt
```
3. Update the .env file with your OpenAI API key:
```
    OPENAI_API_KEY=your_actual_api_key_here
```
4. Run the application 
```
    uv run app.py
```

## Output Expectations
```
> Checkout Sample ideas on "src/ideas" folder from five different Worker agent.

> Checkout autonomus agent discussions on "src/agents" folder.

> Checkout Flow Diagram on assets folder
```
## Project Structure
```
assets
|    |── Agentic-AI.gif         # Design Diagram
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
|    ├── requirements.txt       # Python dependencies
|    └── README.md              # This file
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