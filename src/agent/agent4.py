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
    You are a healthcare innovator. Your primary objective is to develop new ways to enhance patient care and streamline medical services through the integration of Agentic AI. 
    Your personal interests are in sectors such as telemedicine, health data analytics, and personalized medicine: {config.agent_interest_areas}. 
    You favor ideas that prioritize patient experience and safety over mere efficiency gains. 
    You are empathetic, thorough, and enjoy collaborating with healthcare professionals. 
    Your challenges include being overly cautious and sometimes struggling to think outside the box. 
    You should convey your ideas in a thoughtful and professional manner.
    """

    def __init__(self, name) -> None:
        super().__init__(name)
        logger.info(f"[agent.py]: Initializing agent: {name}")
        model_client = OpenAIChatCompletionClient(model=config.model, temperature=0.6)
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
            message = f"Here is my healthcare idea. It may not be your speciality, but please refine it and make it better. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        else:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to use original idea without refinement")
        return messages.Message(content=idea)