# Drug Recommendation & Treatment Decision Support System

A production-oriented clinical decision-support prototype where a user enters a sample patient profile and receives ranked candidate treatments with supporting evidence, contraindication checks, allergy warnings, drug-interaction checks, and transparent explanations. The project is split into a FastAPI backend and a React TypeScript frontend, with synthetic clinical data, a content-based recommendation engine, safety rules, PostgreSQL-ready infrastructure, and Docker Compose deployment.

> This is a clinical decision-support prototype, not an autonomous prescribing tool. It uses synthetic data and inspectable rules for portfolio and learning purposes. Real clinical use requires approved datasets, local guideline review, pharmacovigilance data, clinician oversight, governance, monitoring, and regulatory validation.

![Clinical decision-support dashboard](docs/screenshots/clinical-decision-support.png)

## Features

- Clinical profile form for age, sex, diagnosis, symptoms, severity, allergies, comorbidities, current medicines, and pregnancy status
- Synthetic medical dataset with diagnoses, medicine attributes, patient characteristics, contraindications, interaction groups, and treatment outcomes
- Supervised treatment-outcome models trained from synthetic historical cases
- Random Forest baseline model for tabular outcome prediction
- XGBoost model for boosted-tree treatment success prediction
- Content-based treatment ranking using TF-IDF vectorization and cosine similarity
- Rule alignment score based on diagnosis match, symptom match, and first-line status
- Synthetic treatment outcome priors used as an additional relevance signal
- Allergy checks for medicine-specific and class-level risks
- Contraindication checks for comorbidities, pregnancy, age restrictions, and configured clinical risk groups
- Drug-interaction checks using normalized medication and interaction groups
- Monitoring warnings for severe presentations and renal-risk scenarios
- Candidate, caution, and blocked recommendation states
- Explanation trail for every recommendation, including model similarity, rule alignment, synthetic outcome prior, and evidence tier
- Saved model artifacts for repeatable FastAPI inference
- FastAPI OpenAPI documentation
- React TypeScript interface with responsive clinical workflow layout
- Docker Compose stack for backend, frontend, and PostgreSQL
- PostgreSQL initialization placeholder for audit-event storage
- Backend unit tests for safety rules and recommendation ranking

## Screenshots

### Clinical Profile And Recommendations

![Clinical profile and ranked treatments](docs/screenshots/clinical-decision-support.png)

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Lucide React icons
- CSS modules-style plain stylesheet

### Backend

- Python
- FastAPI
- Pydantic
- pandas
- scikit-learn
- XGBoost
- NumPy
- joblib
- SQLAlchemy-ready configuration
- Uvicorn
- Pytest

### Infrastructure

- Docker Compose
- PostgreSQL
- Synthetic CSV dataset generation
- Environment-based configuration

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py              # API endpoints for metadata and recommendations
│   │   ├── core/
│   │   │   └── config.py              # Environment and CORS settings
│   │   ├── schemas/
│   │   │   └── clinical.py            # Pydantic request and response models
│   │   ├── services/
│   │   │   ├── recommender.py         # TF-IDF ranking and recommendation explanations
│   │   │   └── safety.py              # Allergy, contraindication, interaction checks
│   │   ├── ml/
│   │   │   ├── features.py            # Supervised ML feature engineering
│   │   │   ├── outcome_model.py       # Saved model loading and prediction
│   │   │   └── artifacts/             # Random Forest, XGBoost, metrics, best model
│   │   └── main.py                    # FastAPI app entrypoint
│   ├── data/
│   │   ├── medicines.csv              # Synthetic medicine attributes and safety metadata
│   │   └── treatment_cases.csv        # Synthetic historical-style treatment outcomes
│   ├── scripts/
│   │   ├── generate_synthetic_data.py # Dataset generator
│   │   └── train_outcome_models.py    # Random Forest and XGBoost training
│   ├── tests/
│   │   ├── test_recommender.py
│   │   └── test_safety.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts              # Typed API client
│   │   ├── components/
│   │   │   ├── ProfileForm.tsx        # Clinical input workflow
│   │   │   ├── RecommendationResults.tsx
│   │   │   └── SafetyBadge.tsx
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── styles.css
│   │   ├── types.ts
│   │   └── vite-env.d.ts
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs/
│   └── screenshots/
│       └── clinical-decision-support.png
├── infra/
│   └── db/
│       └── init.sql                   # PostgreSQL audit table placeholder
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Architecture

The backend is organized around explicit clinical decision-support responsibilities rather than a single large application file.

`schemas` owns the public request and response contracts for clinical profiles, recommendations, and safety issues.

`services.recommender` owns dataset loading, TF-IDF vectorization, similarity scoring, outcome-prior scoring, ranking, confidence assignment, and explanation generation.

`services.safety` owns deterministic safety checks for allergies, contraindications, age limits, pregnancy-sensitive medicines, renal monitoring, severe acuity notes, and interaction groups.

`ml.features` owns supervised feature engineering for patient-medicine pairs.

`ml.outcome_model` owns loading the saved best model and predicting treatment success probability at API runtime.

`api.routes` exposes the clinical metadata endpoint and the recommendation endpoint.

The frontend keeps the clinical workflow separated into a profile form, recommendation results view, safety badges, shared API client, and shared TypeScript models.

## Recommendation Flow

1. The user enters a sample clinical profile in the React UI.
2. The frontend posts the profile to `POST /api/recommendations`.
3. The backend converts diagnosis, symptoms, severity, and comorbidities into a clinical query.
4. The trained XGBoost/Random Forest model predicts treatment success probability for each patient-medicine pair.
5. TF-IDF compares the profile query against medicine indication text, symptom text, drug class, and mechanism.
6. Rule scoring rewards diagnosis match, symptom match, and first-line status.
7. Synthetic outcome priors from generated treatment cases adjust ranking.
8. Safety rules evaluate allergies, contraindications, pregnancy, age restrictions, current medicines, interaction groups, and monitoring needs.
9. The API returns ranked recommendations with ML probability, status, score, confidence, evidence tier, explanation text, and safety issues.

## Machine Learning Models

The project now uses supervised tabular ML in addition to content-based recommendation logic.

### Training Target

The model predicts whether a patient-medicine case is likely to have a successful outcome.

Successful outcomes:

- `resolved`
- `improved`

Non-success outcomes:

- `unchanged`
- `adverse_event`

### Model Candidates

- `random_forest` using `RandomForestClassifier`
- `gradient_boosting_xgboost_style` using scikit-learn gradient boosting fallback
- `xgboost` using `XGBClassifier`

The training script evaluates each model and saves the best model by ROC-AUC and F1.

### Features

The supervised model uses:

- Age
- Sex
- Diagnosis
- Severity
- Candidate medicine
- Drug class
- Route
- First-line flag
- Minimum age
- Age-below-minimum flag
- Diagnosis match
- Symptom match ratio
- Symptom count
- Allergy count
- Comorbidity count
- Current medication count
- Pregnancy flag

### Saved Artifacts

Model artifacts are saved in:

```text
backend/app/ml/artifacts/
```

Current artifacts include:

- `best_outcome_model.joblib`
- `random_forest.joblib`
- `xgboost.joblib`
- `gradient_boosting_xgboost_style.joblib`
- `metrics.json`

Train or retrain the models with:

```bash
cd backend
python scripts/train_outcome_models.py
```

The recommendation engine combines scores as:

```text
40% supervised ML success probability
30% content similarity
20% clinical rule alignment
10% synthetic outcome prior
```

## Dataset

The included dataset is synthetic and intended only for prototype development.

### Medicines Dataset

`backend/data/medicines.csv` contains:

- Medicine ID and name
- Drug class
- Route
- Supported diagnoses
- Symptom profile
- Mechanism text
- Contraindications
- Interaction groups
- Allergy terms
- Minimum age
- First-line flag
- Evidence tier

### Treatment Cases Dataset

`backend/data/treatment_cases.csv` contains generated historical-style cases:

- Case ID
- Patient age and sex
- Diagnosis
- Symptoms
- Medicine ID
- Severity
- Outcome
- Adverse event marker

Regenerate the data with:

```bash
cd backend
python scripts/generate_synthetic_data.py
```

After regenerating data, retrain the ML models:

```bash
python scripts/train_outcome_models.py
```

## Local Setup

### Prerequisites

- Python 3.12+
- Node.js 22+
- Docker Desktop, optional for full stack
- PostgreSQL, optional when running outside Docker

## 1. Configure Environment

Copy the example environment file if you want to customize local settings:

```bash
copy .env.example .env
```

Important values:

```env
DATABASE_URL=postgresql+psycopg://clinical:clinical@localhost:5432/clinical_support
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
VITE_API_BASE_URL=http://localhost:8000
```

Never commit real secrets or patient data.

## 2. Start Backend Locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python scripts/train_outcome_models.py
uvicorn app.main:app --reload
```

The backend runs at:

- API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

If port `8000` is blocked, use another port:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8010
```

## 3. Start Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at:

- `http://localhost:5173`
- `http://127.0.0.1:5173`

If the backend uses a custom port:

```bash
set VITE_API_BASE_URL=http://127.0.0.1:8010
npm run dev
```

## 4. Start The Docker Stack

```bash
docker compose up --build
```

The Docker stack exposes:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Backend docs: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

## API Endpoints

### System

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Backend health check |

### Clinical Decision Support

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/metadata` | Lists sample diagnoses, symptoms, comorbidities, medicines, and allergies for the UI |
| POST | `/api/recommendations` | Returns ranked candidate treatments with evidence and safety warnings |

## Example Recommendation Request

```bash
curl -X POST http://localhost:8000/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "age": 52,
    "sex": "female",
    "diagnosis": "type 2 diabetes",
    "symptoms": ["elevated glucose", "fatigue", "polyuria"],
    "allergies": [],
    "comorbidities": ["hypertension"],
    "current_medications": ["amlodipine"],
    "pregnant": false,
    "severity": "moderate"
  }'
```

Example top candidate:

```json
{
  "medicine_name": "Metformin",
  "drug_class": "Biguanide antihyperglycemic",
  "ml_success_probability": 0.83,
  "recommendation_status": "candidate",
  "confidence": "moderate"
}
```

## Safety Model

The prototype uses explicit safety checks before presenting recommendations.

### Blocking Issues

- Recorded allergy matches medicine or drug class
- Patient comorbidity matches configured contraindication
- Pregnancy conflicts with configured pregnancy contraindication
- Patient age is below configured minimum age

### Warning Issues

- Current medications map to configured interaction groups
- Current therapy overlaps with anticoagulant, antiplatelet, SSRI, NSAID, lithium, or hypoglycemic risk groups

### Monitoring Issues

- Renal monitoring signals
- Severe presentation requiring urgent clinician assessment

Blocked recommendations can still appear in the response when useful for showing why a medicine is unsafe.

## Development Commands

Run backend tests:

```bash
cd backend
python -m pytest
```

Compile backend Python files:

```bash
cd backend
python -m compileall app scripts
```

Run frontend typecheck and production build:

```bash
cd frontend
npm run build
```

Regenerate synthetic data:

```bash
cd backend
python scripts/generate_synthetic_data.py
```

Retrain supervised ML models:

```bash
cd backend
python scripts/train_outcome_models.py
```

Run full stack:

```bash
docker compose up --build
```

Stop Docker services:

```bash
docker compose down
```

Reset Docker database volume:

```bash
docker compose down -v
```

## Verification

The current implementation was checked with:

```bash
cd backend
python -m pytest
```

```bash
cd frontend
npm run build
```

Manual smoke test:

- Started backend on `http://127.0.0.1:8010`
- Started frontend on `http://127.0.0.1:5173`
- Submitted the default diabetes profile
- Confirmed ranked treatment results rendered in the browser
- Confirmed Metformin appeared as the top candidate

## Production Notes

Before any production or real clinical deployment:

- Replace synthetic data with approved formularies, approved drug databases, and locally reviewed clinical guidelines
- Add clinician-reviewed validation and safety test sets
- Add authentication, authorization, and audit logging
- Add protected PHI handling, encryption, retention rules, and privacy controls
- Add full PostgreSQL persistence for profiles, recommendation events, audit trails, and model versions
- Add pharmacovigilance-grade drug interaction and contraindication sources
- Add model monitoring, drift detection, and continuous safety evaluation
- Add CI/CD with backend tests, frontend build, dependency scanning, and container scanning
- Add HTTPS, strict CORS, secure headers, and deployment secrets management
- Add structured logging and error monitoring such as OpenTelemetry or Sentry
- Add clinician sign-off workflow before recommendations can influence care

## Clinical Disclaimer

This project does not diagnose, prescribe, or replace professional medical judgment. It is a prototype for demonstrating recommendation-system architecture, clinical rule checks, and explainable decision-support UI patterns. Any real use must be supervised by qualified clinicians and governed by applicable laws, regulations, and institutional policies.

## License

This project is provided as a portfolio and learning prototype. Add a license before using it in a commercial, public production, or clinical context.
