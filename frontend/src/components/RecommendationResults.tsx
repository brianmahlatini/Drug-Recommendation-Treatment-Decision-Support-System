import { ShieldCheck, Stethoscope } from "lucide-react";
import type { RecommendationResponse } from "../types";
import { MonitorBadge, SafetyBadge } from "./SafetyBadge";

type Props = {
  response: RecommendationResponse | null;
  error: string | null;
};

export function RecommendationResults({ response, error }: Props) {
  if (error) {
    return <section className="panel error-panel">{error}</section>;
  }

  if (!response) {
    return (
      <section className="empty-state">
        <Stethoscope size={34} aria-hidden="true" />
        <h2>No Review Yet</h2>
        <p>Enter a sample profile to generate ranked treatment candidates and safety notes.</p>
      </section>
    );
  }

  return (
    <section className="results" aria-label="Recommendation results">
      <div className="results-header">
        <div>
          <h2>Candidate Treatments</h2>
          <p>{response.profile_summary}</p>
        </div>
        <ShieldCheck size={28} aria-hidden="true" />
      </div>

      <div className="disclaimer">{response.disclaimer}</div>

      <div className="recommendation-list">
        {response.recommendations.map((recommendation) => (
          <article className="recommendation-card" key={recommendation.medicine_id}>
            <header>
              <div>
                <h3>{recommendation.medicine_name}</h3>
                <p>{recommendation.drug_class} · {recommendation.route}</p>
              </div>
              <SafetyBadge status={recommendation.recommendation_status} />
            </header>

            <div className="score-row">
              <span>Score {(recommendation.score * 100).toFixed(0)}%</span>
              <span>Confidence {recommendation.confidence}</span>
            </div>
            <div className="score-track">
              <div style={{ width: `${Math.max(4, recommendation.score * 100)}%` }} />
            </div>

            <div className="evidence">{recommendation.evidence_level}</div>

            <div className="detail-grid">
              <div>
                <h4>Explanation</h4>
                <ul>
                  {recommendation.explanation.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h4>Safety</h4>
                {recommendation.safety_issues.length === 0 ? (
                  <p className="clear-safety">No prototype rule warnings triggered.</p>
                ) : (
                  <ul>
                    {recommendation.safety_issues.map((issue) => (
                      <li key={`${issue.category}-${issue.message}`}>
                        {issue.severity === "monitor" ? <MonitorBadge /> : null}
                        <span>{issue.message}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

