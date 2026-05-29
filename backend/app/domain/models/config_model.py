from pydantic import BaseModel, field_validator, model_validator
from typing import List
from app.domain.enums.enums import ProviderType, StrategyType
from app.domain.models.models import Timeframes

class ConfigModel(BaseModel):
    provider: ProviderType = ProviderType.MT5
    symbols: List[str]
    strategy: StrategyType
    timeframes: Timeframes
    execution_interval: int

    @field_validator("execution_interval")
    def validate_interval(cls, v):
        if v < 10:
            raise ValueError("Execution interval must be greater or equal to 10")
        return v

    @field_validator("strategy")
    def validate_strategy(cls, v):
        if not v:
            raise ValueError("Strategy must be selected")
        return v

    @field_validator("timeframes")
    def validate_timeframes(cls, v):
        if not v.trend or not v.entry:
            raise ValueError("Values trend and entry timeframes are required")

        return v

    @model_validator(mode="after")
    def validate_cross_fields(self):
        if self.timeframes.trend == self.timeframes.entry:
            raise ValueError("Trend and Entry timeframes must be different")

        if not self.symbols or len(self.symbols) == 0:
            raise ValueError("At least one symbol is required")

        return self
