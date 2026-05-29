import "./SignalPanel.scss";

function LogPanel({ logs }) {
  return (
    <div className="container-table logs-table">
        <table className="signals-table">
            <thead>
                <tr>
                    <th>Type</th>
                    <th>Time</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
                {logs.map((log, i) => (
                <tr key={i}>
                    <td>{log.level}</td>
                    <td>{new Date(log.timestamp).toLocaleTimeString()}</td>
                    <td>{log.message}</td>
                </tr>
                ))}
            </tbody>
        </table>
    </div>
  );
}

export default LogPanel;
