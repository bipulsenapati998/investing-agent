from dataclasses import dataclass
import json
import os

@dataclass
class Config:
    config_version: str
    model: str
    temperature: float
    no_of_agents: int
    port: int
    host: str
    bounce_probability_to_another_agent: float
    agent_interest_areas: list[str]
    
    @staticmethod
    def load(path=None) -> "Config":
        if path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(current_dir, "../../"))
            path = os.path.join(project_root, "config.json")
        with open(path) as f:
            data = json.load(f)
        return Config(
            config_version=data.get("config_version", "1.0"),
            model=data.get("model", "gpt-4o-mini"),
            temperature=data.get("temperature", 0.8),
            no_of_agents=data.get("no_of_agents", 2),
            port=data.get("port", 50051),
            host=data.get("host", "localhost"),
            bounce_probability_to_another_agent=data.get("bounce_idea_to_another_agent", 0.5),
            agent_interest_areas=data.get("agent_interest_areas", ["insurance", "Personal Financial"]),
        )
