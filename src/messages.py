from dataclasses import dataclass
from autogen_core import AgentId
import glob
import os
import random
from config.logger_config import get_messages_logger

logger = get_messages_logger()

@dataclass
class Message:
    content: str


def find_recipient() -> AgentId:
    try:
        logger.debug("[message.py]: Searching for available agents to use as recipients")
        agent_files = glob.glob("agent/agent*.py")
        agent_names = [os.path.splitext(os.path.basename(file))[0] for file in agent_files]
        if "agent" in agent_names:
            agent_names.remove("agent")
        agent_name = random.choice(agent_names)
        logger.info(f"[message.py]: Selected agent for refinement: {agent_name}")
        return AgentId(agent_name, "default")
    except Exception as e:
        logger.error(f"[message.py]: Exception finding recipient: {e}", exc_info=True)
        return AgentId("agent1", "default")
