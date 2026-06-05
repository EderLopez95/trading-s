import "./StatusBar.scss";
import { BotStatus } from "../enums";

function StatusBar({ status }) {
  return (
    <div className={`status ${status === BotStatus.RUNNING ? "running" : status === BotStatus.STOPPED ? "stopped" : "unknown"}`}>
      Bot status: {status}
    </div>
  );
}

export default StatusBar;
