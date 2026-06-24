# SmartHire AI Run Instructions

## 1. Start the backend

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8000
```

Backend URL: `http://localhost:8000`

Useful checks:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/candidates
Invoke-RestMethod http://localhost:8000/jobs
```

## 2. Start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

The frontend defaults to `http://localhost:8000` for the API. To use a different backend URL, create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 3. Data files used

The backend reads project data from:

- `data/candidates.csv`
- `data/jobs.csv`

The frontend does not use local mock data. It loads candidates, jobs, health, and JD parsing through the FastAPI backend.
