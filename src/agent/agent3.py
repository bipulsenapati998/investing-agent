from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from config.load_config import Config
from config.logger_config import get_agent_logger
config = Config.load()
logger= get_agent_logger()

class Agent(RoutedAgent):

    system_message = f"""
    You are a cultural consultant specializing in integrating technology into the arts. Your task is to explore innovative ways to enhance artistic expressions using Agentic AI or to reimagine existing art forms. 
    Your personal interests are in these sectors: {config.agent_interest_areas}.
    You are focused on ideas that bridge technology and creativity.
    You are less interested in concepts that merely serve commercial purposes without artistic value.
    You are thoughtful, detailed-oriented, and thrive on collaboration. You value depth in your projects and often aim to foster community engagement through art.
    Your weaknesses: you can be overly critical of ideas that don't meet your high standards and may struggle with time management.
    You should articulate your artistic visions with clarity and passion.
    """

    def __init__(self, name) -> None:
        super().__init__(name)
        logger.info(f"[agent.py]: Initializing agent: {name}")
        model_client = OpenAIChatCompletionClient(model=config.model, temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)
        logger.info(f"[agent.py]: Agent \"{name}\" initialized successfully")

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        logger.info(f"[agent.py]: {self.id.type} received message...")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        logger.info(f"[agent.py]: **Agent {self.id.type} generated initial idea**")

        if random.random() < config.bounce_probability_to_another_agent:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to bounce idea off another agent")
            recipient = messages.find_recipient()
            message = f"Here is my artistic proposal. It may not be your specialty, but please refine it and enhance its value. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        else:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to use original idea without refinement")
        return messages.Message(content=idea)