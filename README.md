# SmartHire AI 🚀

**Merit First. Intelligence Always.**

A bias-aware, AI-powered recruitment system that ranks candidates using semantic understanding, skill matching, career progression analysis, and application quality assessment. Unlike traditional ATS systems that rely on keywords and referrals, SmartHire AI produces explainable, fair candidate rankings using embeddings and vector search.

---

## 🎯 Core Features

✅ **Semantic Understanding** - AI understands job requirements and candidate profiles meaningfully  
✅ **Bias-Free Ranking** - Referral information removed before ranking, revealed only as metadata after  
✅ **FAISS Vector Search** - Fast semantic search across thousands of candidates  
✅ **Explainable Rankings** - Every candidate ranking includes reasoning  
✅ **Scalable Architecture** - Designed for enterprise-scale recruiting  
✅ **Production-Ready** - Comprehensive logging, error handling, and validation  

---

## 📐 Architecture

### Ranking Pipeline

```
Job Description
      ↓
JD Parser (Extract: role, skills, experience, education, seniority)
      ↓
BGE Embedding Model (BAAI/bge-large-en-v1.5)
      ↓
FAISS Vector Search (Retrieve Top 100 Candidates)
      ↓
Bias Removal Layer (Remove: employee_id, referred_by, referral_flag, manager_name)
      ↓
Signal Fusion Ranking
      final_score = α·semantic + β·skill + γ·career + δ·clean_activity
      ↓
Explainability Engine ("Why was this candidate ranked here?")
      ↓
Ranked Candidate List (with referral metadata shown AFTER ranking only)
```

### Fair Ranking Principle

**Referral information MUST NOT influence ranking.**

1. Normal and referred candidates enter the same pipeline
2. Bias fields removed before embedding and ranking
3. Ranking happens fairly and transparently
4. Referral metadata revealed only in final output

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Embeddings**: Sentence Transformers (BAAI/bge-large-en-v1.5)
- **Vector DB**: FAISS (CPU-optimized)
- **Data Processing**: Pandas, NumPy, Scikit-learn
- **Async**: Uvicorn, Pydantic
- **Deployment**: Docker, Docker Compose

### Key Libraries
```
fastapi==0.104.1           # Web framework
sentence-transformers==2.2.2  # Embeddings
faiss-cpu==1.7.4           # Vector search
pandas==2.1.3              # Data handling
torch==2.1.1               # ML framework
```

---

## 📊 Ranking Formula

```
final_score = α × semantic_score + β × skill_score + γ × career_score + δ × clean_activity

Default Weights:
- α (semantic):    0.4  (40%) - How well profile matches JD semantically
- β (skill):       0.3  (30%) - How many required skills are present
- γ (career):      0.2  (20%) - Experience, education, projects, certifications
- δ (activity):    0.1  (10%) - Clean profile (not spam, complete, genuine)
```

### Score Definitions

| Score | Meaning | Calculation |
|-------|---------|-------------|
| **Semantic** | Profile-JD semantic similarity | Cosine similarity of embeddings |
| **Skill** | Required skills present | matched_skills / total_required_skills |
| **Career** | Career progression & fit | Experience + Education + Projects + Certifications |
| **Activity** | Profile authenticity | 0.0-1.0 penalty for suspicious behavior |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip / virtualenv
- 4GB+ RAM (for BGE model)

### Installation

1. **Clone repository**
```bash
git clone <your-repo>
cd smarthire-ai
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment**
```bash
# .env file is already created with defaults
# Customize if needed
cp .env .env.local
```

5. **Create sample data**
```bash
python -c "from app.db.database import Database; Database.create_sample_candidates()"
```

6. **Run FastAPI server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Access API**
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🐳 Docker Deployment

### Run with Docker

```bash
# Build image
docker build -t smarthire-ai:latest .

# Run container
docker run -p 8000:8000 -v $(pwd)/data:/app/data smarthire-ai:latest
```

### Run with Docker Compose

```bash
# Start services
docker-compose up --build

# Stop services
docker-compose down
```

Access at: http://localhost:8000/docs

---

## 📡 API Endpoints

### 1. Health Check
```http
GET /health
```
Returns service status.

### 2. Parse Job Description
```http
POST /parse-jd
Content-Type: application/json

{
  "jd": "Senior Backend Engineer with 5+ years Python, FastAPI, Docker..."
}
```
**Response:**
```json
{
  "role": "Backend Engineer",
  "skills": ["Python", "FastAPI", "Docker", "AWS"],
  "experience": 5,
  "education": "BTech",
  "seniority": "Senior",
  "certifications": ["AWS Certified"]
}
```

### 3. Get All Candidates
```http
GET /candidates
```
**Response:**
```json
{
  "total": 5,
  "candidates": [
    {
      "id": "cand_001",
      "name": "John Doe",
      "skills": "Python, FastAPI, Docker",
      "experience": 5,
      "education": "BTech",
      "activity_score": 0.95
    }
  ]
}
```

### 4. Rank Candidates (Core Endpoint)
```http
POST /rank
Content-Type: application/json

{
  "jd": "Senior Backend Engineer with 5+ years Python, FastAPI, Docker, AWS..."
}
```
**Response:**
```json
{
  "total": 5,
  "results": [
    {
      "rank": 1,
      "id": "cand_001",
      "name": "John Doe",
      "semantic_score": 0.92,
      "skill_score": 0.88,
      "career_score": 0.84,
      "clean_activity": 0.95,
      "final_score": 0.90,
      "explanation": "Strong backend experience with Python, FastAPI, Docker. 5 years relevant experience. Consistent career growth."
    }
  ]
}
```

---

## 📁 Project Structure

```
smarthire-ai/
├── backend/
│   └── app/
│       ├── api/
│       │   └── routes/
│       │       ├── health.py          # Health check endpoint
│       │       ├── jd.py              # JD parsing endpoint
│       │       ├── candidate.py        # Candidates list endpoint
│       │       └── rank.py             # Main ranking endpoint
│       ├── services/
│       │   ├── jd_parser.py            # JD extraction (regex-based)
│       │   ├── embedding_service.py    # BGE embeddings
│       │   ├── faiss_service.py        # FAISS index operations
│       │   └── bias_removal_service.py # Fair ranking
│       ├── schemas/
│       │   ├── jd_schema.py            # Pydantic models for JD
│       │   └── candidate_schema.py     # Pydantic models for candidates
│       ├── db/
│       │   └── database.py             # Data access layer
│       ├── utils/
│       │   ├── config.py               # Configuration
│       │   └── logger.py               # Logging setup
│       └── main.py                     # FastAPI app initialization
├── data/
│   ├── candidates.csv                  # Candidate database
│   ├── faiss_index.bin                 # FAISS index (generated)
│   └── faiss_id_mapping.pkl            # ID mappings (generated)
├── docs/
│   └── output/
│       └── ranked_output.csv           # Ranking results
├── tests/                              # Unit tests (coming soon)
├── .env                                # Environment configuration
├── .gitignore                          # Git ignore rules
├── Dockerfile                          # Docker build config
├── docker-compose.yml                  # Docker Compose config
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

## 🧪 Testing

### Manual Testing via Swagger

1. Open http://localhost:8000/docs
2. Try out endpoints in the interactive UI

### Sample JD for Testing

```
Senior Backend Engineer
5+ years of experience

Required Skills:
- Python
- FastAPI
- Docker
- AWS
- PostgreSQL

Education: BTech in Computer Science or equivalent
Seniority: Senior
Certifications: AWS Certified preferred
```

---

## 📋 Configuration

Edit `.env` to customize:

```env
# API Configuration
API_PORT=8000
API_HOST=0.0.0.0

# Embedding Model
MODEL_NAME=BAAI/bge-large-en-v1.5
DEVICE=cpu  # or 'cuda' for GPU

# FAISS Settings
TOP_K=100  # Retrieve top 100 candidates

# Ranking Weights (must sum to ~1.0)
ALPHA=0.4   # Semantic score weight
BETA=0.3    # Skill match weight
GAMMA=0.2   # Career score weight
DELTA=0.1   # Activity score weight

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

---

## 🔄 Team Responsibilities

### Ashish (AS) - Backend/AI Lead
- ✅ FastAPI setup
- ✅ JD Parser
- ✅ Embedding Service
- ✅ FAISS Integration
- ✅ Bias Removal
- ✅ Docker deployment
- ⏳ Integration with scoring_service.py (from CH)

### Chaturya (CH) - Ranking & Explainability
- 🔜 scorer.py (skill, career, activity scoring)
- 🔜 rerank_service.py (sophisticated reranking)
- 🔜 explanation_service.py (detailed explanations)

### Other Team Members
- 🔜 Frontend (React dashboard)
- 🔜 Data Engineering (ETL pipeline)
- 🔜 DevOps (CI/CD setup)

---

## 🏆 Hackathon Winning Strategy

1. **Fairness First** - Emphasize bias removal in pitch
2. **Semantic Understanding** - Show JD-candidate semantic matching
3. **Explainability** - Every ranking has reasoning
4. **Scalability** - FAISS can handle 100k+ candidates
5. **Production Ready** - Logging, error handling, tests
6. **Live Demo** - Working API with Swagger UI

---

## 🤝 Integration with CH's Modules

When `scoring_service.py`, `rerank_service.py`, and `explanation_service.py` are ready:

```python
# In rank.py, update:
from app.services.scoring_service import calculate_scores
from app.services.rerank_service import rerank
from app.services.explanation_service import generate_explanation

# For each result:
scores = calculate_scores(candidate, jd_data)
result['semantic_score'] = scores['semantic']
result['skill_score'] = scores['skill']
result['career_score'] = scores['career']
result['clean_activity'] = scores['activity']
result['final_score'] = scores['final']
result['explanation'] = generate_explanation(candidate, scores)
```

---

## 📝 Logging

All services log to console with timestamps:

```
2024-01-15 10:30:45 - SmartHire - INFO - Starting JD parsing...
2024-01-15 10:30:46 - SmartHire - INFO - Extracted role: Backend Engineer
```

For debugging, set `LOG_LEVEL=DEBUG` in `.env`

---

## 🐛 Troubleshooting

### Issue: "Module not found" error
**Solution**: Activate virtual environment and reinstall dependencies
```bash
pip install -r requirements.txt
```

### Issue: Port 8000 already in use
**Solution**: Change port in command
```bash
uvicorn app.main:app --port 8001
```

### Issue: BGE model download fails
**Solution**: Model downloads on first use (~300MB). Ensure internet connectivity.

### Issue: FAISS index errors
**Solution**: Delete `data/faiss_index.bin` and `data/faiss_id_mapping.pkl`, restart

---

## 📚 References

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **BGE Model**: https://huggingface.co/BAAI/bge-large-en-v1.5
- **FAISS**: https://github.com/facebookresearch/faiss
- **Sentence Transformers**: https://www.sbert.net/

---

## 📞 Support & Questions

For issues or questions:
1. Check logs: `LOG_LEVEL=DEBUG`
2. Review API docs: http://localhost:8000/docs
3. Test endpoints in Swagger UI

---

## 🎓 Learning Resources

### How This Works

1. **Embedding** - Text → 1024-dim vector using BGE
2. **Indexing** - Vectors → FAISS index for fast search
3. **Search** - Find top-k similar candidates
4. **Scoring** - Calculate multiple relevance scores
5. **Ranking** - Combine scores with weights
6. **Explanation** - Describe why candidate ranked

### Why This Matters

- **Fair**: No referrals bias ranking
- **Fast**: FAISS searches 100k candidates in milliseconds
- **Smart**: Semantic understanding, not keyword matching
- **Explainable**: Know exactly why a candidate was ranked
- **Scalable**: Handles growth to millions of candidates

---

## 📄 License

SmartHire AI - Open Source Hackathon Project

---

## 🙏 Acknowledgments

Built for the recruitment hackathon with focus on:
- AI fairness and bias removal
- Semantic search and embeddings
- Production-ready code
- Team collaboration

**"Merit First. Intelligence Always."** 🚀

