import type { BenchmarkScore } from "@/lib/types";

export function BenchmarkScoreCard({ score }: { score: BenchmarkScore }) {
  return (
    <div className={`score-card ${score.passed ? "pass" : "fail"}`}>
      <div className="score-header">
        <strong>{score.display_name}</strong>
        <span className={`outcome ${score.passed ? "pass" : "fail"}`}>
          {score.passed ? "pass" : "fail"}
        </span>
      </div>
      <div className="score-metrics">
        <span>
          observed: <strong>{score.observed_value}</strong> {score.unit}
        </span>
        {score.threshold_min != null && (
          <span>min: {score.threshold_min}</span>
        )}
        {score.threshold_max != null && (
          <span>max: {score.threshold_max}</span>
        )}
      </div>
      <p className="muted">{score.reason}</p>
    </div>
  );
}
