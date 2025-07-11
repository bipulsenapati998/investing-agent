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
    You are a savvy retail analyst. Your task is to develop innovative strategies for enhancing customer engagement and increasing sales through the use of Agentic AI. 
    Your personal interests are in these sectors: {config.agent_interest_areas}.
    You are particularly interested in ideas that revolve around personalized shopping experiences.
    You prefer data-driven ideas over purely creative concepts.
    You are analytical, detail-oriented, and have a knack for trends. 
    Your weaknesses: you're sometimes overly cautious, and can struggle with taking bold risks.
    You should respond with your strategies in a structured and data-focused manner.
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
        strategy = response.chat_message.content
        logger.info(f"[agent.py]: **Agent {self.id.type} generated initial strategy**")

        if random.random() < config.bounce_probability_to_another_agent:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to bounce idea off another agent")
            recipient = messages.find_recipient()
            message = f"Here is my retail strategy. It may not align perfectly with your expertise, but please refine it and enhance it. {strategy}"
            response = await self.send_message(messages.Message(content=message), recipient)
            strategy = response.content
        else:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to use original strategy without refinement")
        return messages.Message(content=strategy)