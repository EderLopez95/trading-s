import { startBot, stopBot } from "../services/api";
import "./BotControl.scss";
import { useContext } from "react";
import { AppContext } from "../App";
import { BotStatus } from "../enums";

function BotControl() {
  const { showToast, setStatus } = useContext(AppContext);
  
  const handleStart = async () => {
    try {
      const response = await startBot();

      if (response.status === BotStatus.RUNNING) {
        setStatus(BotStatus.RUNNING);
        showToast("info", "Bot is running");
      }
    }
    catch (err) {
      console.error("Error starting bot:", err);
      showToast("error", "Error starting bot");
    }
  };

  const handleStop = async () => {
    try {
      const response = await stopBot();
      
      if (response.status === BotStatus.STOPPED) {
        setStatus(BotStatus.STOPPED);
        showToast("info", "Bot is stopped");
      }
    }
    catch (err) {
      console.error("Error stopping bot:", err);
      showToast("error", "Error stopping bot");
    }
  };

  return (
    <div className="bot-controls">
      <button className="stop" onClick={handleStop}>
        Stop
      </button>
      <button className="start" onClick={handleStart}>
        Start
      </button>
    </div>
  );
}

export default BotControl;
