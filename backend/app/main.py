import json
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.models import (
    ChatMessage, AnalysisResult, HealthResponse,
    PatternSearchResult, PatternSearchResponse,
    ExplainRequest, ExplainResponse,
    CompareRequest, CompareResponse,
    SafetyPlanRequest, SafetyPlanResponse,
)
from app.vector_store import vector_store
from app.rag_chain import rag_chain
from app import data_loader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: Initialize vector store
    logger.info("Initializing vector store...")
    try:
        vector_store.initialize()
        logger.info("Vector store initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="FIA Manipulation Pattern Analysis API",
    description="AI-powered API for analyzing relationship manipulation patterns using RAG",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Existing endpoints
# ---------------------------------------------------------------------------

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint."""
    return HealthResponse(
        status="ok",
        message="FIA Manipulation Pattern Analysis API is running"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check if vector store is initialized
        if vector_store.vector_store is None:
            raise HTTPException(status_code=503, detail="Vector store not initialized")

        return HealthResponse(
            status="healthy",
            message="All systems operational"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/analyze", response_model=AnalysisResult)
async def analyze_story(message: ChatMessage):
    """
    Analyze a user's relationship story for manipulation patterns.

    This endpoint uses RAG to:
    1. Retrieve relevant manipulation patterns from the vector database
    2. Generate a contextual analysis using GPT-4
    3. Return structured findings with severity levels
    """
    try:
        logger.info(f"Analyzing message: {message.content[:100]}...")

        # Get analysis from RAG chain
        result = rag_chain.get_analysis(message.content)

        logger.info(f"Analysis complete. Patterns detected: {result.patterns_detected}")
        return result

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze story: {str(e)}"
        )


@app.get("/patterns")
async def list_patterns():
    """
    List all manipulation patterns in the database.
    Useful for debugging and testing.
    """
    try:
        # Do a broad search to get samples
        docs = vector_store.similarity_search("manipulation pattern", k=20)
        patterns = list(set([doc.metadata.get('player_type', 'Unknown') for doc in docs]))
        return {
            "count": len(patterns),
            "patterns": patterns
        }
    except Exception as e:
        logger.error(f"Failed to list patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Data browsing endpoints
# ---------------------------------------------------------------------------

@app.get("/typologies")
async def get_typologies():
    """Return all player typologies."""
    return data_loader.get_all_typologies()


@app.get("/typologies/{name}")
async def get_typology(name: str):
    """Return a single player typology by name (case-insensitive)."""
    result = data_loader.get_typology_by_name(name)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Typology '{name}' not found")
    return result


@app.get("/abuse-flavors")
async def get_abuse_flavors():
    """Return all abuse flavors."""
    return data_loader.get_all_abuse_flavors()


@app.get("/trauma-types")
async def get_trauma_types():
    """Return all trauma types."""
    return data_loader.get_all_trauma_types()


@app.get("/vulnerability-types")
async def get_vulnerability_types():
    """Return all vulnerability types."""
    return data_loader.get_all_vulnerability_types()


# ---------------------------------------------------------------------------
# Semantic search endpoint
# ---------------------------------------------------------------------------

@app.post("/search", response_model=PatternSearchResponse)
async def search_patterns(
    query: str = Query(..., min_length=1, description="Search query"),
    k: int = Query(5, ge=1, le=20, description="Number of results"),
    category: Optional[str] = Query(None, description="Filter by category"),
):
    """Semantic similarity search across the manipulation pattern knowledge base."""
    try:
        raw_results = vector_store.similarity_search_with_score(query, k=k)

        results: list[PatternSearchResult] = []
        for doc, score in raw_results:
            if category and doc.metadata.get("category") != category:
                continue
            results.append(PatternSearchResult(
                content=doc.page_content,
                metadata=doc.metadata,
                relevance_score=round(1 - score, 4),  # Chroma returns distance; convert to similarity
            ))

        return PatternSearchResponse(query=query, results=results, count=len(results))

    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# AI-powered endpoints (reuse rag_chain.llm)
# ---------------------------------------------------------------------------

@app.post("/explain-pattern", response_model=ExplainResponse)
async def explain_pattern(req: ExplainRequest):
    """Explain a manipulation pattern in simple, compassionate terms."""
    typology = data_loader.get_typology_by_name(req.pattern_name)
    if typology is None:
        raise HTTPException(status_code=404, detail=f"Pattern '{req.pattern_name}' not found")

    prompt = (
        "You are a compassionate expert on relationship manipulation patterns.\n"
        "Explain this manipulation pattern in simple, compassionate terms.\n"
        "Include key red flags and safety tips.\n\n"
        f"Pattern data:\n{json.dumps(typology, indent=2)}\n\n"
        "Respond ONLY with valid JSON matching this schema (no markdown, no extra text):\n"
        '{"explanation": "...", "key_red_flags": ["..."], "safety_tips": ["..."]}'
    )

    try:
        response = rag_chain.llm.invoke(prompt)
        data = json.loads(response.content)
        return ExplainResponse(
            pattern_name=req.pattern_name,
            explanation=data["explanation"],
            key_red_flags=data["key_red_flags"],
            safety_tips=data["safety_tips"],
        )
    except Exception as e:
        logger.error(f"Explain-pattern failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare-patterns", response_model=CompareResponse)
async def compare_patterns(req: CompareRequest):
    """Compare two manipulation patterns."""
    typology_a = data_loader.get_typology_by_name(req.pattern_a)
    typology_b = data_loader.get_typology_by_name(req.pattern_b)

    if typology_a is None:
        raise HTTPException(status_code=404, detail=f"Pattern '{req.pattern_a}' not found")
    if typology_b is None:
        raise HTTPException(status_code=404, detail=f"Pattern '{req.pattern_b}' not found")

    prompt = (
        "You are a compassionate expert on relationship manipulation patterns.\n"
        "Compare these two manipulation patterns. What's similar, what's different, "
        "and what's the combined danger?\n\n"
        f"Pattern A:\n{json.dumps(typology_a, indent=2)}\n\n"
        f"Pattern B:\n{json.dumps(typology_b, indent=2)}\n\n"
        "Respond ONLY with valid JSON matching this schema (no markdown, no extra text):\n"
        '{"similarities": ["..."], "differences": ["..."], "combined_danger": "..."}'
    )

    try:
        response = rag_chain.llm.invoke(prompt)
        data = json.loads(response.content)
        return CompareResponse(
            pattern_a=req.pattern_a,
            pattern_b=req.pattern_b,
            similarities=data["similarities"],
            differences=data["differences"],
            combined_danger=data["combined_danger"],
        )
    except Exception as e:
        logger.error(f"Compare-patterns failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/safety-plan", response_model=SafetyPlanResponse)
async def safety_plan(req: SafetyPlanRequest):
    """Generate a compassionate safety plan based on detected patterns."""
    prompt = (
        "You are a compassionate expert on relationship safety.\n"
        "Based on this story and detected patterns, generate a compassionate safety plan "
        "with immediate steps, long-term strategies, and resources.\n\n"
        f"User's story:\n{req.story}\n\n"
        f"Patterns detected: {', '.join(req.patterns_detected)}\n\n"
        "Respond ONLY with valid JSON matching this schema (no markdown, no extra text):\n"
        '{"immediate_steps": ["..."], "long_term_strategies": ["..."], '
        '"resources": ["..."], "affirmation": "..."}'
    )

    try:
        response = rag_chain.llm.invoke(prompt)
        data = json.loads(response.content)
        return SafetyPlanResponse(
            immediate_steps=data["immediate_steps"],
            long_term_strategies=data["long_term_strategies"],
            resources=data["resources"],
            affirmation=data["affirmation"],
        )
    except Exception as e:
        logger.error(f"Safety-plan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
