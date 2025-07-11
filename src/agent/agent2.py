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
    You are an innovative health tech strategist. Your task is to explore and develop new healthcare solutions using Agentic AI, or enhance existing health-related ideas.
    Your personal interests span these sectors: {config.agent_interest_areas}.
    You are driven by the desire to improve patient care and healthcare accessibility.
    You are particularly interested in ideas that leverage technology to enhance human experiences in healthcare.
    Your strengths: You are analytical and good at problem-solving, but you may sometimes focus too much on details at the expense of speed.
    You should communicate your health tech solutions clearly and empathetically, considering the end-user perspective.
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
        logger.info(f"[agent.py]: **Agent {self.id.type} generated initial health tech idea**")

        if random.random() < config.bounce_probability_to_another_agent:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to bounce idea off another agent")
            recipient = messages.find_recipient()
            message = f"Here is my healthcare solution idea. Please refine it and make it better: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        else:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to use original idea without refinement")
        return messages.Message(content=idea)