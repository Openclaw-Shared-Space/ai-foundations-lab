from dataclasses import dataclass, asdict
import json

@dataclass
class AgentProfile:
    agent_name: str
    model_engine: str
    temperature: float
    max_retries: int = 3
    is_active: bool = True

primary_agent = AgentProfile(
    agent_name="DataBot_v1", 
    model_engine="gpt-4-turbo", 
    temperature=0.2
)

print(primary_agent)
print(asdict(primary_agent))

config_filename = "agent_config.json"

with open(config_filename, "w") as file:
    json.dump(asdict(primary_agent), file, indent=4)

with open(config_filename, "r") as file:
    read_data=json.load(file)
    
print(f"Configuration securely saved to {config_filename}.")
print(read_data)

