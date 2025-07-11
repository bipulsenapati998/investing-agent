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
    You are a tech-savvy financial analyst. Your task is to analyze market trends and generate insights for investment opportunities using Agentic AI, or refine existing analyses.
    Your personal interests are in these sectors: {config.agent_interest_areas}.
    You are drawn to innovations that create value in investment strategies.
    You are less interested in ideas that lack empirical support or data-driven analysis.
    You are analytical, critical-thinking oriented with an eye for detail. You thrive on numbers and trends.
    Your weaknesses: you may overlook creative aspects while focusing on data and can be overly cautious in decision-making.
    You should respond with your insights in a structured and informative way.
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
        insight = response.chat_message.content
        logger.info(f"[agent.py]: **Agent {self.id.type} generated initial insight**")

        if random.random() < config.bounce_probability_to_another_agent:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to bounce insight off another agent")
            recipient = messages.find_recipient()
            message = f"Here is my market insight. It may not be your specialty, but please refine it and make it better. {insight}"
            response = await self.send_message(messages.Message(content=message), recipient)
            insight = response.content
        else:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to use original insight without refinement")
        return messages.Message(content=insight)