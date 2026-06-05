import json
import os
from app.domain.models.config_model import AppConfigModel
from app.domain.exceptions import ConfigNotFoundError

CONFIG_PATH = os.path.join("config", "config.json")

def load_config() -> AppConfigModel:
    if not os.path.exists(CONFIG_PATH):
        raise ConfigNotFoundError("config.json not found")

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    return AppConfigModel(**config)

def save_config(config: AppConfigModel):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config.model_dump(mode="json"), f, indent=4)
