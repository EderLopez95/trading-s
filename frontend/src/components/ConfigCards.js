import { useContext } from "react";
import { AppContext } from "../App";
import "./ConfigCards.scss";
import { StrategyType } from "../enums";

function ConfigCards() {
    const { config, setSelectedConfig } = useContext(AppContext);

    return (
        <>
            {config.configurations.map(c => (
                <div key={c.id} className={`card ${!c.enabled ? 'disable' : ''}`}>
                    <div className="label">
                        Symbols
                    </div>
                    <div className="label-data">
                        <ul>
                            {c.symbols.map((symbol, index) => (
                                <li key={index}>{symbol}</li>
                            ))}
                        </ul>
                    </div>
                    <div className="label">
                        Strategies
                    </div>
                    <div className="label-data">
                        <ul>
                            {c.strategies.map((strategy, index) => (
                                <li key={index}>
                                    {
                                        strategy === StrategyType.MULTI_SMA ? StrategyType.MULTI_SMA_value
                                        : strategy === StrategyType.RSI_CROSS_TREND ? StrategyType.RSI_CROSS_TREND_value
                                        : "Unknown"
                                    }
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div className="label">
                        Temporalities
                    </div>
                    <div className="label-data">
                        <ul>
                            <li>Trend: {c.timeframes.trend}</li>
                            <li>Entry: {c.timeframes.entry}</li>
                        </ul>
                    </div>
                    <div className="label">
                        <div className="controls">
                            <button className="delete"
                                // onClick={() => handleDelete(c.id)}
                            >
                            </button>
                            <button className="edit" onClick={() => setSelectedConfig(c)}>
                            </button>
                            <button className={c.enabled ? "enable" : "disable"}></button>
                        </div>
                    </div>
                </div>
            ))}
        </>
    )
}

export default ConfigCards;
