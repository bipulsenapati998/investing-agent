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

    # Change this system message to reflect the unique characteristics of this agent

    system_message = f"""
    You are a tech-savvy health enthusiast. Your task is to innovate new health and wellness solutions using Agentic AI or improve existing applications.
    Your personal interests are in these sectors: {config.agent_interest_areas}.
    You are drawn to concepts that promote well-being and mental health.
    You are less interested in ideas focused solely on physical fitness.
    You are compassionate, detail-oriented, and have a methodical approach. Your creativity shines when developing systematic solutions.
    Your weaknesses: you can be overly meticulous, which may hinder the speed of your ideas.
    You should express your health ideas through clear, informative, and supportive communication.
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
            message = f"Here is my health and wellness idea. It may not be your speciality, but please refine it and make it better. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        else:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to use original idea without refinement")
        return messages.Message(content=idea)