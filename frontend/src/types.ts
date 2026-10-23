export type ClinicalProfile = {
  age: number;
  sex: "female" | "male" | "intersex" | "unknown";
  diagnosis: string;
  symptoms: string[];
  allergies: string[];
  comorbidities: string[];
  current_medications: string[];
  pregnant: boolean;
  severity: "mild" | "moderate" | "severe";
};

export type SafetyIssue = {
  severity: "block" | "warning" | "monitor";
  category: string;
  message: string;
};

export type Recommendation = {
  medicine_id: string;
  medicine_name: string;
  drug_class: string;
  route: string;
  score: number;
  confidence: "low" | "moderate" | "high";
  evidence_level: string;
  recommendation_status: "candidate" | "use_with_caution" | "blocked";
  explanation: string[];
  safety_issues: SafetyIssue[];
};

export type RecommendationResponse = {
  disclaimer: string;
  profile_summary: string;
  recommendations: Recommendation[];
};

export type Metadata = {
  diagnoses: string[];
  symptoms: string[];
  comorbidities: string[];
  medicines: string[];
  allergies: string[];
};

