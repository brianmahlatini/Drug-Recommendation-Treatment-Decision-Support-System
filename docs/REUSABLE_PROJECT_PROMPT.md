# Reusable Full-Stack ML Project Prompt

Use this prompt when you want to build or redo a senior-level ML web application with separate backend, frontend, data, model training, tests, Docker, README, and GitHub push.

```text
Build this project at senior portfolio level as a full-stack application.

Project:
[PASTE PROJECT TITLE]

Objective:
[PASTE PROJECT OBJECTIVE]

Requirements:
- Separate backend and frontend folders.
- Backend must use Python, FastAPI, Pydantic, pandas, scikit-learn, and a real supervised ML model where appropriate.
- If the project is tabular prediction or recommendation, include at least:
  - RandomForestClassifier baseline
  - XGBoost model if suitable
  - Feature engineering module
  - Training script
  - Saved model artifacts
  - Metrics JSON
  - Runtime prediction service loaded by the API
- If recommendation logic is needed, combine:
  - Supervised ML prediction score
  - Content similarity or domain relevance score
  - Rule-based validation or safety checks
  - Transparent explanations for each recommendation
- Frontend must use React, TypeScript, Vite, separate components, typed API client, and a polished responsive interface.
- Include generated sample data if no approved dataset is provided.
- Include tests for backend model/prediction logic.
- Include Dockerfiles and docker-compose.yml.
- Include .env.example and .gitignore.
- Write a complete GitHub README in portfolio format:
  - Summary
  - Screenshot
  - Features
  - Tech stack
  - Project structure
  - Architecture
  - ML model details
  - Dataset details
  - Local setup
  - Docker setup
  - API endpoints
  - Example request/response
  - Development commands
  - Verification
  - Production notes
  - Disclaimer or license notes when relevant
- Run verification:
  - backend tests
  - backend compile check
  - frontend production build
  - browser or API smoke test where possible
- Commit and push to this GitHub repository:
  [PASTE GITHUB REPOSITORY URL]

Important:
- Do not build only a UI mockup.
- Do not claim ML if only rules are used.
- If XGBoost cannot be installed locally, implement Random Forest plus a gradient boosting fallback and document the limitation clearly.
- Keep generated dependency folders, build output, caches, and local tool artifacts out of Git.
```

For clinical or high-stakes projects, add this instruction:

```text
This is a decision-support prototype only. It must not be presented as autonomous medical, legal, or financial advice. Add explicit disclaimers, auditability, explanations, and production safety notes.
```

