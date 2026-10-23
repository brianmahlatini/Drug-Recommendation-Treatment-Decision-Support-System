import { useEffect, useState } from "react";
import { Database, HeartPulse } from "lucide-react";

import { getMetadata, getRecommendations } from "./api/client";
import { ProfileForm } from "./components/ProfileForm";
import { RecommendationResults } from "./components/RecommendationResults";
import type { ClinicalProfile, Metadata, RecommendationResponse } from "./types";

const initialProfile: ClinicalProfile = {
  age: 52,
  sex: "female",
  diagnosis: "type 2 diabetes",
  symptoms: ["elevated glucose", "fatigue", "polyuria"],
  allergies: [],
  comorbidities: ["hypertension"],
  current_medications: ["amlodipine"],
  pregnant: false,
  severity: "moderate"
};

function App() {
  const [profile, setProfile] = useState<ClinicalProfile>(initialProfile);
  const [metadata, setMetadata] = useState<Metadata | null>(null);
  const [response, setResponse] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getMetadata()
      .then(setMetadata)
      .catch(() => setMetadata(null));
  }, []);

  async function submit() {
    setLoading(true);
    setError(null);
    try {
      setResponse(await getRecommendations(profile));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to generate recommendations.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <HeartPulse size={30} aria-hidden="true" />
          <div>
            <h1>Treatment Decision Support</h1>
            <p>Recommendation engine with transparent clinical safety checks</p>
          </div>
        </div>
        <div className="dataset-pill">
          <Database size={17} aria-hidden="true" />
          Synthetic dataset
        </div>
      </header>

      <div className="workspace">
        <ProfileForm profile={profile} metadata={metadata} loading={loading} onChange={setProfile} onSubmit={submit} />
        <RecommendationResults response={response} error={error} />
      </div>
    </main>
  );
}

export default App;

