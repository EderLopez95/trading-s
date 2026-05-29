class DomainError(Exception):
    pass

class InvalidConfigError(DomainError):
    pass

class StrategyNotFoundError(DomainError):
    pass

class ConfigNotFoundError(DomainError):
    pass

class BotAlreadyRunningError(DomainError):
    pass

class BotNotRunningError(DomainError):
    pass
