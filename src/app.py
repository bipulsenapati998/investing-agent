from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
from agent import Agent
from creator import Creator
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from autogen_core import AgentId
import messages
import asyncio
from dotenv import load_dotenv
import os
from config.load_config import Config
from config.logger_config import get_app_logger
config = Config.load()
logger = get_app_logger()

load_dotenv(override=True)

async def create_and_message(worker, creator_id, i: int):
    try:
        logger.info(f"[app.py]: Starting to create agent{i} and generate idea")
        result = await worker.send_message(messages.Message(content=f"agent{i}.py"), creator_id)
        idea_folder = "idea"
        os.makedirs(idea_folder, exist_ok=True)
        
        # Save idea file to idea folder
        idea_file_path = f"{idea_folder}/idea{i}.md"
        with open(idea_file_path, "w") as f:
            f.write(result.content)
        logger.info(f"[app.py]: Successfully saved idea{i}.md to {idea_file_path}")
    except Exception as e:
        logger.error(f"[app.py]: Failed to run worker {i} due to exception: {e}", exc_info=True)

async def main():
    agent_folder = "agent"
    os.makedirs(agent_folder, exist_ok=True)
    logger.info(f"[app.py]: Created agent folder: {agent_folder}")

    logger.info("[app.py]: Starting gRPC worker agent runtime host")
    host = GrpcWorkerAgentRuntimeHost(address=f"{config.host}:{config.port}",)
    host.start() 

    logger.info("[app.py]: Starting gRPC worker agent runtime")
    worker = GrpcWorkerAgentRuntime(host_address=f"{config.host}:{config.port}")
    await worker.start()

    logger.info("[app.py]: Registering Creator agent")
    result = await Creator.register(worker, "Creator", lambda: Creator("Creator"))
    creator_id = AgentId("Creator", "default")

    logger.info(f"[app.py]: Creating {config.no_of_agents} agents and generating ideas")
    routines = [create_and_message(worker, creator_id, i) for i in range(1, config.no_of_agents+1)]
    await asyncio.gather(*routines)
    logger.info("All agents created and ideas generated successfully")

    try:
        logger.info("[app.py]: Stopping worker and host")
        await worker.stop()
        await host.stop()
    except Exception as e:
        logger.error(f"[app.py]: Error during shutdown: {e}", exc_info=True)


if __name__ == "__main__":
    logger.info("Starting Business Investing Agent Application")
    asyncio.run(main())
