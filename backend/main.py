"""
PRAJNA — FastAPI Backend
========================

Backend foundation for the PRAJNA Crime Intelligence Platform.

Part 1 provides:
- FastAPI application
- CORS configuration
- API route structure
- Mock database integration
- Network graph API
- FIR lookup
- Suspect lookup
- Placeholder integration points for Part 2 engines

The query, memory, and pressure logic will be connected to:
- query_engine.py
- memory_weaving.py
- pressure_engine.py

when Part 2 is integrated.
"""

from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from mock_db import (
    get_active_alerts,
    get_all_firs,
    get_all_suspects,
    get_fir_by_id,
    get_network_data,
    get_suspect_by_id,
)


# ---------------------------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------------------------

app = FastAPI(
    title="PRAJNA Crime Intelligence Platform",
    description=(
        "Predictive Reasoning & Adaptive Justice Network for Action — "
        "KSP Datathon 2026"
    ),
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------------------------------

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    language: str = Field(default="en-IN")
    officer_id: str = Field(default="OFFICER-DEMO")
    session_id: str = Field(default="SESSION-DEMO")


class MemoryRequest(BaseModel):
    officer_id: str
    query: str
    response: Dict[str, Any]
    outcome: str = "unclassified"


# ---------------------------------------------------------------------------
# ROOT / HEALTH
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    """Basic API information endpoint."""
    return {
        "application": "PRAJNA",
        "description": "Predictive Reasoning & Adaptive Justice Network for Action",
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
def health_check():
    """Health check endpoint for local and Catalyst deployment."""
    return {
        "status": "healthy",
        "service": "prajna-api",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# POST /api/query
# ---------------------------------------------------------------------------

@app.post("/api/query")
def process_query(request: QueryRequest):
    """
    Process an investigator query.

    Part 2 will connect this endpoint to query_engine.py.

    The fallback response keeps the API functional until the query engine
    is integrated.
    """

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )

    return {
        "answer": (
            "The PRAJNA query engine is ready to process this investigation "
            "query. The intelligent mock query engine will be connected in "
            "Part 2."
        ),
        "nodes": [],
        "edges": [],
        "cited_firs": [],
        "memory_thread_id": None,
        "query": query,
        "language": request.language,
        "officer_id": request.officer_id,
        "session_id": request.session_id,
    }


# ---------------------------------------------------------------------------
# GET /api/network
# ---------------------------------------------------------------------------

@app.get("/api/network")
def get_network():
    """
    Return the complete criminal intelligence network.

    The response is compatible with the D3.js Case Canvas.
    """

    return get_network_data()


# ---------------------------------------------------------------------------
# GET /api/fir/{fir_id}
# ---------------------------------------------------------------------------

@app.get("/api/fir/{fir_id}")
def get_fir(fir_id: str):
    """Return detailed information about a specific FIR."""

    fir = get_fir_by_id(fir_id)

    if fir is None:
        raise HTTPException(
            status_code=404,
            detail=f"FIR '{fir_id}' was not found.",
        )

    return fir


# ---------------------------------------------------------------------------
# GET /api/suspect/{id}
# ---------------------------------------------------------------------------

@app.get("/api/suspect/{suspect_id}")
def get_suspect(suspect_id: str):
    """
    Return a suspect profile with linked FIR information.
    """

    suspect = get_suspect_by_id(suspect_id)

    if suspect is None:
        raise HTTPException(
            status_code=404,
            detail=f"Suspect '{suspect_id}' was not found.",
        )

    linked_firs = [
        get_fir_by_id(fir_id)
        for fir_id in suspect["linked_firs"]
    ]

    suspect["linked_fir_details"] = [
        fir
        for fir in linked_firs
        if fir is not None
    ]

    return suspect


# ---------------------------------------------------------------------------
# GET /api/pressure
# ---------------------------------------------------------------------------

@app.get("/api/pressure")
def get_pressure():
    """
    Return crime pressure data.

    Part 2 will connect this endpoint to pressure_engine.py.

    The fallback response returns the base zone data so that the frontend
    can be developed independently.
    """

    from mock_db import PRESSURE_ZONES

    return {
        "zones": [
            {
                **zone,
                "pressure_score": 0.0,
                "pressure_level": "unavailable",
                "breakdown": {
                    "bail_release_score": 0.0,
                    "festival_score": 0.0,
                    "economic_stress_score": 0.0,
                    "infrastructure_score": 0.0,
                },
                "explanation": (
                    "The pressure engine will calculate the zone score "
                    "when Part 2 is integrated."
                ),
                "patrol_recommendation": (
                    "Awaiting pressure engine calculation."
                ),
            }
            for zone in PRESSURE_ZONES
        ],
        "weights": {
            "bail_releases": 0.4,
            "festivals": 0.3,
            "economic_stress": 0.2,
            "infrastructure": 0.1,
        },
    }


# ---------------------------------------------------------------------------
# POST /api/memory
# ---------------------------------------------------------------------------

@app.post("/api/memory")
def save_memory(request: MemoryRequest):
    """
    Save an investigator memory thread.

    Part 2 will connect this endpoint to memory_weaving.py.

    For Part 1, the endpoint validates and returns the memory payload.
    """

    thread_id = (
        f"MEM-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
    )

    return {
        "success": True,
        "memory_thread_id": thread_id,
        "officer_id": request.officer_id,
        "query": request.query,
        "response": request.response,
        "outcome": request.outcome,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": (
            "Memory thread accepted. Persistent Memory Weaving storage "
            "will be connected in Part 2."
        ),
    }


# ---------------------------------------------------------------------------
# GET /api/memory/{officer_id}
# ---------------------------------------------------------------------------

@app.get("/api/memory/{officer_id}")
def get_memory(officer_id: str):
    """
    Retrieve memory threads for an officer.

    Part 2 will connect this endpoint to persistent Memory Weaving storage.
    """

    return {
        "officer_id": officer_id,
        "threads": [],
        "count": 0,
        "message": (
            "No persistent memory threads are available yet. "
            "Memory Weaving will be integrated in Part 2."
        ),
    }


# ---------------------------------------------------------------------------
# GET /api/alerts
# ---------------------------------------------------------------------------

@app.get("/api/alerts")
def get_alerts():
    """
    Return active crime pressure anomaly alerts.
    """

    alerts = get_active_alerts()

    return {
        "alerts": alerts,
        "count": len(alerts),
    }


# ---------------------------------------------------------------------------
# OPTIONAL DATA ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/api/suspects")
def get_suspects():
    """Return all suspects."""
    return {
        "suspects": get_all_suspects(),
        "count": len(get_all_suspects()),
    }


@app.get("/api/firs")
def get_firs():
    """Return all FIRs."""
    return {
        "firs": get_all_firs(),
        "count": len(get_all_firs()),
    }