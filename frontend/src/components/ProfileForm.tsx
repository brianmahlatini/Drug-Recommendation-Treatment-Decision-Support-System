import { Activity, AlertTriangle, ClipboardPlus, Send } from "lucide-react";
import type { ClinicalProfile, Metadata } from "../types";

type Props = {
  profile: ClinicalProfile;
  metadata: Metadata | null;
  loading: boolean;
  onChange: (profile: ClinicalProfile) => void;
  onSubmit: () => void;
};

const fallbackDiagnoses = ["type 2 diabetes", "hypertension", "asthma", "gerd", "community acquired pneumonia"];

function parseList(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

export function ProfileForm({ profile, metadata, loading, onChange, onSubmit }: Props) {
  const diagnoses = metadata?.diagnoses.length ? metadata.diagnoses : fallbackDiagnoses;

  return (
    <section className="panel profile-panel" aria-label="Clinical profile">
      <div className="section-heading">
        <ClipboardPlus size={22} aria-hidden="true" />
        <div>
          <h2>Clinical Profile</h2>
          <p>Sample patient details for decision-support ranking.</p>
        </div>
      </div>

      <div className="form-grid">
        <label>
          Age
          <input
            type="number"
            min={0}
            max={120}
            value={profile.age}
            onChange={(event) => onChange({ ...profile, age: Number(event.target.value) })}
          />
        </label>

        <label>
          Sex
          <select value={profile.sex} onChange={(event) => onChange({ ...profile, sex: event.target.value as ClinicalProfile["sex"] })}>
            <option value="female">Female</option>
            <option value="male">Male</option>
            <option value="intersex">Intersex</option>
            <option value="unknown">Unknown</option>
          </select>
        </label>

        <label>
          Severity
          <select
            value={profile.severity}
            onChange={(event) => onChange({ ...profile, severity: event.target.value as ClinicalProfile["severity"] })}
          >
            <option value="mild">Mild</option>
            <option value="moderate">Moderate</option>
            <option value="severe">Severe</option>
          </select>
        </label>

        <label className="span-2">
          Diagnosis
          <input
            list="diagnosis-options"
            value={profile.diagnosis}
            onChange={(event) => onChange({ ...profile, diagnosis: event.target.value })}
          />
          <datalist id="diagnosis-options">
            {diagnoses.map((diagnosis) => (
              <option value={diagnosis} key={diagnosis} />
            ))}
          </datalist>
        </label>

        <label className="span-2">
          Symptoms
          <textarea
            value={profile.symptoms.join(", ")}
            onChange={(event) => onChange({ ...profile, symptoms: parseList(event.target.value) })}
          />
        </label>

        <label>
          Allergies
          <textarea
            value={profile.allergies.join(", ")}
            onChange={(event) => onChange({ ...profile, allergies: parseList(event.target.value) })}
          />
        </label>

        <label>
          Comorbidities
          <textarea
            value={profile.comorbidities.join(", ")}
            onChange={(event) => onChange({ ...profile, comorbidities: parseList(event.target.value) })}
          />
        </label>

        <label className="span-2">
          Current Medicines
          <textarea
            value={profile.current_medications.join(", ")}
            onChange={(event) => onChange({ ...profile, current_medications: parseList(event.target.value) })}
          />
        </label>
      </div>

      <div className="form-footer">
        <label className="toggle">
          <input
            type="checkbox"
            checked={profile.pregnant}
            onChange={(event) => onChange({ ...profile, pregnant: event.target.checked })}
          />
          Pregnancy recorded
        </label>

        <button type="button" onClick={onSubmit} disabled={loading || !profile.diagnosis.trim()}>
          {loading ? <Activity className="spin" size={18} /> : <Send size={18} />}
          Review candidates
        </button>
      </div>

      <div className="clinical-note">
        <AlertTriangle size={18} aria-hidden="true" />
        <span>Prototype output must be reviewed by a qualified clinician.</span>
      </div>
    </section>
  );
}

