import Link from "next/link";
import { loadRegistryData } from "@/lib/data";

export default function ExecutionsPage() {
  const data = loadRegistryData();
  const executions = [...data.executions].sort(
    (a, b) => new Date(b.started_at).getTime() - new Date(a.started_at).getTime(),
  );

  return (
    <>
      <div className="page-header">
        <h1>Executions</h1>
        <p>{executions.length} runtime execution records</p>
      </div>
      <table className="registry-table">
        <thead>
          <tr>
            <th>Run</th>
            <th>Agent</th>
            <th>Model</th>
            <th>Status</th>
            <th>Benchmark score</th>
            <th>Started</th>
          </tr>
        </thead>
        <tbody>
          {executions.map((execution) => {
            const runs = data.benchmarkRuns.filter((r) => r.run_id === execution.run_id);
            const meanScore =
              runs.length > 0
                ? (runs.reduce((sum, r) => sum + r.observed_value, 0) / runs.length).toFixed(2)
                : "—";
            return (
              <tr key={execution.run_id}>
                <td>
                  <Link href={`/executions/${encodeURIComponent(execution.run_id)}`}>
                    <strong>{execution.run_id}</strong>
                  </Link>
                </td>
                <td>
                  <Link href={`/agents/${encodeURIComponent(execution.agent_id)}`}>
                    {execution.agent_id}
                  </Link>
                </td>
                <td>{execution.model_id ?? "—"}</td>
                <td>
                  <span className={`outcome ${execution.status}`}>{execution.status}</span>
                </td>
                <td>{meanScore}</td>
                <td>{new Date(execution.started_at).toLocaleString()}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}
