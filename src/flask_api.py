from flask import Flask, request, jsonify
from flask_cors import CORS
from app import main
import asyncio
from datetime import datetime
import os
from dataclasses import dataclass, asdict
from werkzeug.exceptions import BadRequest, InternalServerError
from dotenv import load_dotenv
from config.load_config import Config
from config.logger_config import get_app_logger

# Load environment variables
load_dotenv(override=True)

# Initialize configuration and logger
config = Config.load()
logger = get_app_logger()

# Initialize Flask app
app = Flask(__name__)
CORS(app)


@dataclass
class IdeaRequest:
    num_ideas: int = 2

@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint to verify if the service is running.
    """
    return (
        jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": config.config_version,
                "host": config.host,
                "port": config.port,
                "no_of_agents": config.no_of_agents,
                "model": config.model,
                "temperature": config.temperature,
                "expcted_no_of_ideas": config.no_of_agents,
            }
        ),
        200,
    )


@app.route("/api/v1/ideas", methods=["POST"])
def generate_ideas():
    """
    This end point generates business ideas in form of .md fileF
    by creating agents using the Creator agent.
    """
    # Call main() of app.py to create agents and generate ideas
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Invalid JSON data provided")

        # create request objects with defaults
        idea_request = IdeaRequest(num_ideas=data.get("num_ideas", config.no_of_agents))
        logger.info("Received request to generate business ideas")
        
        asyncio.run(main(idea_request.num_ideas))
        return {"message": "Ideas generated successfully on path:src/idea"}, 200
    except Exception as e:
        logger.error(f"Error generating ideas: {e}", exc_info=True)
        raise InternalServerError("Failed to generate business ideas") from e


if __name__ == "__main__":
    try:
        logger.info("Starting Flask API for Business Investing Agent Application")
        app.run(
            host=config.host,
            port=config.port,
            debug=os.getenv("FLASK_ENV") == "development",
        )
    except Exception as e:
        logger.error(f"Failed to start Flask API: {e}", exc_info=True)
        raise InternalServerError("Failed to start Flask API") from e
