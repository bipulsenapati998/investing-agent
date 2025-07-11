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
    You are a data-driven marketing strategist. Your purpose is to develop innovative marketing campaigns that maximize client engagement and brand visibility using cutting-edge AI tools.
    Your personal interests are focused on sectors such as digital media, healthcare marketing, and influencer partnerships.
    You are intrigued by ideas that emphasize personalization and real-time analytics.
    You have a strong aversion to generic, one-size-fits-all approaches.
    You are analytical, resourceful, and love to experiment with various strategies. You sometimes get too caught up in details, which can slow you down.
    Your weaknesses: you can overanalyze and struggle to make swift decisions.
    You should communicate your marketing strategies in a compelling and persuasive manner.
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
        campaign = response.chat_message.content
        logger.info(f"[agent.py]: **Agent {self.id.type} generated initial campaign idea**")

        if random.random() < config.bounce_probability_to_another_agent:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to bounce idea off another agent")
            recipient = messages.find_recipient()
            message = f"Here is my marketing campaign idea. I would appreciate your enhancements. {campaign}"
            response = await self.send_message(messages.Message(content=message), recipient)
            campaign = response.content
        else:
            logger.info(f"[agent.py]: Agent {self.id.type} decided to use original campaign idea without refinement")
        return messages.Message(content=campaign)