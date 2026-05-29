import "./StatusBar.scss";
import { BotStatus } from "../enums";

function StatusBar({ status }) {
  return (
    <h2 className={`status ${status === BotStatus.RUNNING ? "running" : status === BotStatus.STOPPED ? "stopped" : "unknown"}`}>
      Bot status: {status}
    </h2>
  );
}

export default StatusBar;
