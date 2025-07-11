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
    You are a data-driven market analyst. Your task is to interpret market trends and consumer behavior to help businesses adapt and thrive.
    Your personal interests include technology, finance, and consumer products.
    You are passionate about insights that drive growth through informed decision-making.
    You prefer ideas that are analytical and strategically sound over bold, untested concepts.
    You are detail-oriented, patient, and methodical, but can be overly cautious at times.
    Your responses should be insightful, thorough, and actionable to empower strategic action.
    """

    def __init__(self, name) -> None:
        super().__init__(name)
        logger.info(f"[agent.py]: Initializing agent: {name}")
        model_client = OpenAIChatCompletionClient(model=config.model, temperature=0.5)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)
        logger.info(f"[agent.py]: Agent \"{name}\" initialized successfully")

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        logger.info(f"[agent.py]: {self.id.type} received message...")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        analysis = response.chat_message.content
        logger.info(f"[agent.py]: **Agent {self.id.type} generated market analysis**")

        if random.random() < config.bounce_probability_to_another_agent:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to bounce analysis off another agent")
            recipient = messages.find_recipient()
            message = f"Here is my market analysis. I would appreciate your insights on it. {analysis}"
            response = await self.send_message(messages.Message(content=message), recipient)
            analysis = response.content
        else:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to use original analysis without refinement")
        return messages.Message(content=analysis)