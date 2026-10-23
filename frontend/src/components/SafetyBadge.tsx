import { AlertOctagon, AlertTriangle, CheckCircle2, Eye } from "lucide-react";
import type { Recommendation } from "../types";

type Props = {
  status: Recommendation["recommendation_status"];
};

export function SafetyBadge({ status }: Props) {
  if (status === "blocked") {
    return (
      <span className="badge blocked">
        <AlertOctagon size={16} /> Blocked
      </span>
    );
  }

  if (status === "use_with_caution") {
    return (
      <span className="badge caution">
        <AlertTriangle size={16} /> Caution
      </span>
    );
  }

  return (
    <span className="badge candidate">
      <CheckCircle2 size={16} /> Candidate
    </span>
  );
}

export function MonitorBadge() {
  return (
    <span className="badge monitor">
      <Eye size={16} /> Monitor
    </span>
  );
}

