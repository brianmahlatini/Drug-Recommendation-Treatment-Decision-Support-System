import type { ClinicalProfile, Metadata, RecommendationResponse } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...init?.headers
    },
    ...init
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getMetadata(): Promise<Metadata> {
  return request<Metadata>("/api/metadata");
}

export function getRecommendations(profile: ClinicalProfile): Promise<RecommendationResponse> {
  return request<RecommendationResponse>("/api/recommendations", {
    method: "POST",
    body: JSON.stringify(profile)
  });
}

