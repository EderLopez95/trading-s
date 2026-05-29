import "./SignalPanel.scss";
import { SignalType, StrategyType } from "../enums";
import { useContext } from "react";
import { AppContext } from "../App";

function SignalPanel({ signals }) {
    const { showToast, setSignals, setLogs } = useContext(AppContext);

    const handleTablesClear = () => {
        localStorage.removeItem("signals");
        localStorage.removeItem("logs");
        setSignals([]);
        setLogs([]);
        showToast("info", "Signals and logs cleared");
    };

    return (
        <div>
            <div className="button-clear">
                <button onClick={handleTablesClear}>
                    Clear
                </button>
            </div>
            <div className="container-table">
                <table className="signals-table">
                    <thead>
                        <tr>
                            <th>Symbol</th>
                            <th>Option</th>
                            <th>Signal</th>
                            <th>Price</th>
                            <th>Strategy</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {signals.map((signal, i) => (
                        <tr key={i}>
                            <td>{signal.symbol}</td>
                            <td className={`${signal.signal === SignalType.BUY ? "buy" : signal.signal === SignalType.SELL ? "sell" : "hold"}`}>
                                {signal.signal === SignalType.BUY ? SignalType.CALL : signal.signal === SignalType.SELL ? SignalType.PUT : SignalType.HOLD}
                            </td>
                            <td className={`${signal.signal === SignalType.BUY ? "buy" : signal.signal === SignalType.SELL ? "sell" : "hold"}`}>
                                {signal.signal}
                            </td>
                            <td>{signal.price}</td>
                            <td>
                                {signal.strategy === StrategyType.MULTI_SMA ? StrategyType.MULTI_SMA_value
                                : signal.strategy === StrategyType.RSI_CROSS_TREND ? StrategyType.RSI_CROSS_TREND_value
                                : "Unknown"}
                            </td>
                            <td>{new Date(signal.timestamp).toLocaleTimeString()}</td>
                        </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default SignalPanel;
