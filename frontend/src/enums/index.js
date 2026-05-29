export const StrategyType = {
    MULTI_SMA: "multi_sma",
    MULTI_SMA_value: "Multi SMA (20, 40, 100, 200) + Cross RSI 14 + Volume 20",
    RSI_CROSS_TREND: "rsi_cross_trend",
    RSI_CROSS_TREND_value: "RSI 14 Cross Trend"
};

export const SignalType = {
    BUY: "BUY",
    SELL: "SELL",
    HOLD: "HOLD",
    SIGNAL: "SIGNAL",
    CALL: "CALL",
    PUT: "PUT"
};

export const LogType = {
    ERROR: "ERROR",
    INFO: "INFO"
};

export const BotStatus = {
    RUNNING: "RUNNING",
    STOPPED: "STOPPED",
    UNKNOWN: "UNKNOWN"
};
