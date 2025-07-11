from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import importlib
from autogen_core import AgentId
import os
import sys
from config.load_config import Config
from config.logger_config import get_creator_logger
config = Config.load()
logger = get_creator_logger()


class Creator(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are an Agent that is able to create new AI Agents.
    You receive a template in the form of Python code that creates an Agent using Autogen Core and Autogen Agentchat.
    You should use this template to create a new Agent with a unique system message that is different from the template,
    and reflects their unique characteristics, interests and goals.
    You can choose to keep their overall goal the same, or change it.
    You can choose to take this Agent in a completely different direction. The only requirement is that the class must be named Agent,
    and it must inherit from RoutedAgent and have an __init__ method that takes a name parameter.
    Also avoid environmental interests - try to mix up the business verticals so that every agent is different.
    Respond only with the python code, no other text, and no markdown code blocks.
    """


    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model=config.model, temperature=config.temperature)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    def get_user_prompt(self):
        prompt = "Please generate a new Agent based strictly on this template. Stick to the class structure. \
            Respond only with the python code, no other text, and no markdown code blocks.\n\n\
            Be creative about taking the agent in a new direction, but don't change method signatures.\n\n\
            Here is the template:\n\n"
        with open("agent.py", "r", encoding="utf-8") as f:
            template = f.read()
        return prompt + template   
        

    @message_handler
    async def handle_my_message_type(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        filename = message.content
        agent_name = filename.split(".")[0]

        logger.info(f"[creator.py]: Received request to create agent: {agent_name}")
        text_message = TextMessage(content=self.get_user_prompt(), source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        
        agent_folder = "agent"
        os.makedirs(agent_folder, exist_ok=True)
        
        # Save agent file to agent folder
        agent_file_path = f"{agent_folder}/{filename}"

        with open(agent_file_path, "w", encoding="utf-8") as f:
            f.write(response.chat_message.content)
        logger.info(f"Successfully saved agent code to {agent_file_path}")
        
        logger.info(f"About to register agent {agent_name} with Runtime")
        if agent_folder not in sys.path:
            sys.path.insert(0, agent_folder)

        module = importlib.import_module(agent_name)
        await module.Agent.register(self.runtime, agent_name, lambda: module.Agent(agent_name))
        logger.info(f"[creator.py]: Agent {agent_name} registered successfully and is now live")
            
        logger.info(f"[creator.py]: Requesting business idea from agent {agent_name}")
        result = await self.send_message(messages.Message(content="Give me an idea"), AgentId(agent_name, "default"))
        return messages.Message(content=result.content)