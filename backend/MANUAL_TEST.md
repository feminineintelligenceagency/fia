# Manual Testing Guide - Python RAG Backend

## Prerequisites

- Python 3.10+ installed
- OpenAI API key

## Step-by-Step Manual Testing

### 1. Install python3-venv (if needed)

```bash
sudo apt install python3.10-venv -y
```

### 2. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Expected output:
```
Successfully installed fastapi-0.115.5 langchain-1.0.5 ...
```

### 5. Configure Environment

```bash
# Copy example env
cp .env.example .env

# Edit .env and add your OpenAI API key
# On Linux/Mac:
nano .env

# On Windows:
notepad .env
```

**Add your key:**
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 6. Ingest Data

```bash
python scripts/ingest_data.py --clear
```

Expected output:
```
================================================================================
FIA Data Ingestion Script - Manipulation Pattern Database
================================================================================

[1/4] Initializing vector store...
✓ Vector store initialized

[2/4] Clearing existing data...

[3/4] Processing data files...

→ Player Typologies (player_typologies.json):
Loading data from data/player_typologies.json...
Processing XX player typologies...
  ✓ Processed: Mr. Always Right
  ✓ Processed: Emotional Predator, Puppet Master, The Svengali
  ...

[4/4] Adding XX total documents to vector store...
✓ All documents added successfully!

🔍 Testing search with query: 'My partner always needs to be right'
[Result 1]
Category: player_typology
Name: Mr. Always Right
Content preview: Player Type: Mr. Always Right...
```

### 7. Start Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 8. Test the API

**Open a new terminal** (keep server running) and test:

#### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "All systems operational"
}
```

#### Test 2: List Patterns (Debug)

```bash
curl http://localhost:8000/patterns
```

Expected response:
```json
{
  "count": 15,
  "patterns": [
    "Mr. Always Right",
    "Emotional Predator, Puppet Master, The Svengali",
    "The Subtle Saboteur",
    ...
  ]
}
```

#### Test 3: Analyze Story

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content": "My partner always needs to be right about everything. When I try to share my opinion, he talks over me or dismisses what I say. He uses a patronizing tone and makes me feel stupid. If I get upset, he says I am being too sensitive."
  }'
```

Expected response (truncated):
```json
{
  "content": "Thank you for sharing your experience. What you're describing shows several concerning patterns...",
  "findings": [
    {
      "type": "danger",
      "title": "Pattern Detected: Mr. Always Right",
      "description": "This behavior pattern matches known manipulation tactics.",
      "matched_pattern": "Mr. Always Right"
    }
  ],
  "patterns_detected": [
    "Mr. Always Right",
    "The Critic"
  ],
  "confidence_score": null
}
```

### 9. Interactive API Testing

Visit: **http://localhost:8000/docs**

This opens Swagger UI where you can:
1. See all API endpoints
2. Test them directly in browser
3. See request/response schemas

## Additional Test Queries

### Test Query 1: Charming Manipulator

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content": "He was so charming at first and made me feel special. But now he isolates me from my friends, checks my phone constantly, and gets angry when I dont do what he wants. He says he loves me but it feels like Im walking on eggshells."
  }'
```

Expected to match: **Emotional Predator, Puppet Master**

### Test Query 2: Guilt-Tripping

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Whenever I try to set boundaries, my partner makes me feel guilty. He says things like after all I have done for you or you are being selfish. I end up apologizing even when I did nothing wrong."
  }'
```

Expected to match: **Guilt-tripper patterns**

### Test Query 3: Control and Criticism

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content": "My partner criticizes everything I do - how I dress, how I talk, my friends, my job. Nothing is ever good enough. He controls all the money and gets angry if I spend anything without asking him first."
  }'
```

Expected to match: **Mr. Always Right, The Demand Man, The Critic**

## Troubleshooting

### Error: "Module not found"
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: "OpenAI API key not found"
```bash
# Check .env file exists
cat .env

# Verify API key is set
grep OPENAI_API_KEY .env

# Make sure there are no spaces or quotes around the key
# Correct: OPENAI_API_KEY=sk-abc123
# Wrong:   OPENAI_API_KEY="sk-abc123"
# Wrong:   OPENAI_API_KEY = sk-abc123
```

### Error: "Vector store not initialized"
```bash
# Re-run data ingestion
python scripts/ingest_data.py --clear
```

### Error: "Port 8000 already in use"
```bash
# Kill existing process
sudo lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --reload --port 8001
```

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Next Steps

Once testing is successful:
1. Integrate with SvelteKit frontend
2. Add authentication
3. Store chat history in Postgres
4. Deploy to production
