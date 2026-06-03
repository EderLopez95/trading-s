import { useContext } from "react";
import { AppContext } from "../App";
import "./ConfigCards.scss";

function ConfigCards() {
    const { config } = useContext(AppContext);

    return (
        <>
            {config.configurations.map(c => (
                <div key={c.id} className="card">
                    <div className="label">
                        Symbols
                    </div>
                    <div className="label-data">
                        {c.symbols.join(", ")}
                    </div>
                    <div className="label">
                        Strategies
                    </div>
                    <div className="label-data">
                        {c.strategies.join(", ")}
                    </div>
                    <div className="label">
                        Temp
                    </div>
                    <div className="label-data">
                        {c.timeframes.trend} / {c.timeframes.entry}
                    </div>
                    <div className="label">
                        {c.enabled && <button>✅</button>}
                        <button
                            // onClick={() => handleEdit(c)}
                        >✏️
                        </button>
                        <button
                            // onClick={() => handleDelete(c.id)}
                        >🗑
                        </button>
                    </div>
                </div>
            ))}
        </>
    )
}

export default ConfigCards;
