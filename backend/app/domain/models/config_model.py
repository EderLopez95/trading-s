from pydantic import BaseModel, field_validator, model_validator
from typing import List
from app.domain.enums.enums import StrategyType
from app.domain.models.models import Timeframes

class ConfigModel(BaseModel):
    id: str
    enabled: bool = True
    symbols: List[str]
    strategies: List[StrategyType]
    timeframes: Timeframes
    
    @model_validator(mode="after")
    def validate_config(self):
        if not self.symbols:
            raise ValueError("At least one symbol is required")
        if len(self.symbols) != len(set(self.symbols)):
            raise ValueError("Duplicate symbols are not allowed")
        if not self.strategies:
            raise ValueError("At least one strategy is required")
        if not self.timeframes.trend or not self.timeframes.entry:
            raise ValueError("Timeframes are required")
        if self.timeframes.trend == self.timeframes.entry:
            raise ValueError("Trend and Entry must be different")
        return self

class AppConfigModel(BaseModel):
    execution_interval: int
    configurations: List[ConfigModel]

    @field_validator("execution_interval")
    def validate_interval(cls, v):
        if v < 30:
            raise ValueError("Execution interval must be greater or equals to 30")
        return v
