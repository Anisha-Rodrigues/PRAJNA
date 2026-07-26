"""
PRAJNA — FastAPI Backend
========================

Predictive Reasoning & Adaptive Justice Network for Action

KSP Datathon 2026
Challenges 01 & 02

This backend integrates:

1. Investigator conversational query engine
2. Criminal intelligence network
3. FIR lookup
4. Suspect lookup
5. Crime pressure analytics
6. Memory Weaving
7. Dissent feedback
8. Anomaly alerts

The current system uses deterministic mock intelligence data and
in-memory Memory Weaving storage.

The architecture is designed so the mock data and memory layer can
later be replaced by persistent Zoho Catalyst storage.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from memory_weaving import (
    create_memory_thread,
    get_memory_summary,
    get_memory_thread,
    get_memory_threads,
    record_dissent,
)

from mock_db import (
    get_active_alerts,
    get_all_firs,
    get_all_suspects,
    get_fir_by_id,
    get_network_data,
    get_suspect_by_id,
)

from pressure_engine import (
    generate_pressure_alerts,
    get_pressure_response,
)

from query_engine import process_query


# ---------------------------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------------------------

app = FastAPI(
    title="PRAJNA Crime Intelligence Platform",
    description=(
        "Predictive Reasoning & Adaptive Justice Network for Action — "
        "KSP Datathon 2026"
    ),
    version="2.0.0",
)


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://prajna-frontend-cesz-ythtpgku.onslate.in",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------------------------------

class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=5000,
    )

    language: str = Field(
        default="en-IN"
    )

    officer_id: str = Field(
        default="OFFICER-DEMO"
    )

    session_id: str = Field(
        default="SESSION-DEMO"
    )


class MemoryRequest(BaseModel):
    officer_id: str = Field(
        ...,
        min_length=1,
    )

    query: str = Field(
        ...,
        min_length=1,
    )

    response: Dict[str, Any] = Field(
        default_factory=dict
    )

    outcome: str = Field(
        default="unclassified"
    )

    session_id: Optional[str] = None


class DissentRequest(BaseModel):
    officer_id: str = Field(
        ...,
        min_length=1,
    )

    session_id: Optional[str] = None

    query: str = Field(
        ...,
        min_length=1,
    )

    response: Dict[str, Any] = Field(
        default_factory=dict
    )

    dissent: bool = True

    note: str = Field(
        default="",
        max_length=2000,
    )


# ---------------------------------------------------------------------------
# ROOT
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    """
    Basic API information endpoint.
    """

    return {
        "application": "PRAJNA",
        "full_name": (
            "Predictive Reasoning & Adaptive Justice Network for Action"
        ),
        "description": (
            "KSP Datathon 2026 Crime Intelligence Platform"
        ),
        "status": "online",
        "version": "2.0.0",
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "modules": [
            "query_engine",
            "crime_network",
            "pressure_engine",
            "memory_weaving",
            "anomaly_alerts",
        ],
    }


# ---------------------------------------------------------------------------
# HEALTH
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """

    return {
        "status": "healthy",
        "service": "prajna-api",
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }


# ---------------------------------------------------------------------------
# POST /api/query
# ---------------------------------------------------------------------------

@app.post("/api/query")
def api_query(
    request: QueryRequest,
):
    """
    Process an investigator query.

    The query engine returns:

    - answer
    - nodes
    - edges
    - cited FIRs

    The complete response is automatically stored in Memory Weaving.
    """

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )

    # Process query with mock AI engine.
    response = process_query(
        query=query,
        language=request.language,
    )

    # Store query/response as a memory thread.
    memory_thread = create_memory_thread(
        officer_id=request.officer_id,
        query=query,
        response=response,
        outcome="unclassified",
        session_id=request.session_id,
    )

    return {
        **response,
        "memory_thread_id": (
            memory_thread[
                "memory_thread_id"
            ]
        ),
        "officer_id": request.officer_id,
        "session_id": request.session_id,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
    }


# ---------------------------------------------------------------------------
# GET /api/network
# ---------------------------------------------------------------------------

@app.get("/api/network")
def get_network():
    """
    Return the complete criminal intelligence graph.

    Compatible with D3.js Case Canvas.
    """

    return get_network_data()


# ---------------------------------------------------------------------------
# GET /api/fir/{fir_id}
# ---------------------------------------------------------------------------

@app.get("/api/fir/{fir_id}")
def get_fir(
    fir_id: str,
):
    """
    Return detailed information about a specific FIR.
    """

    fir = get_fir_by_id(
        fir_id
    )

    if fir is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"FIR '{fir_id}' was not found."
            ),
        )

    return fir


# ---------------------------------------------------------------------------
# GET /api/suspect/{suspect_id}
# ---------------------------------------------------------------------------

@app.get("/api/suspect/{suspect_id}")
def get_suspect(
    suspect_id: str,
):
    """
    Return a suspect profile with complete linked FIR information.
    """

    suspect = get_suspect_by_id(
        suspect_id
    )

    if suspect is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Suspect '{suspect_id}' was not found."
            ),
        )

    linked_firs = [
        get_fir_by_id(
            fir_id
        )
        for fir_id
        in suspect[
            "linked_firs"
        ]
    ]

    suspect[
        "linked_fir_details"
    ] = [
        fir
        for fir in linked_firs
        if fir is not None
    ]

    return suspect


# ---------------------------------------------------------------------------
# GET /api/suspects
# ---------------------------------------------------------------------------

@app.get("/api/suspects")
def get_suspects():
    """
    Return all suspects.
    """

    suspects = get_all_suspects()

    return {
        "suspects": suspects,
        "count": len(
            suspects
        ),
    }


# ---------------------------------------------------------------------------
# GET /api/firs
# ---------------------------------------------------------------------------

@app.get("/api/firs")
def get_firs():
    """
    Return all FIR records.
    """

    firs = get_all_firs()

    return {
        "firs": firs,
        "count": len(
            firs
        ),
    }


# ---------------------------------------------------------------------------
# GET /api/pressure
# ---------------------------------------------------------------------------

@app.get("/api/pressure")
def get_pressure():
    """
    Return calculated crime pressure for all zones.

    Pressure formula:

    Bail Releases       = 40%
    Festivals           = 30%
    Economic Stress     = 20%
    Infrastructure      = 10%
    """

    return get_pressure_response()


# ---------------------------------------------------------------------------
# GET /api/pressure/top
# ---------------------------------------------------------------------------

@app.get("/api/pressure/top")
def get_top_pressure(
    limit: int = Query(
        default=3,
        ge=1,
        le=10,
    ),
):
    """
    Return the highest-pressure zones.
    """

    pressure = get_pressure_response()

    zones = pressure[
        "zones"
    ]

    return {
        "zones": zones[
            :limit
        ],
        "count": min(
            limit,
            len(
                zones
            ),
        ),
    }


# ---------------------------------------------------------------------------
# POST /api/memory
# ---------------------------------------------------------------------------

@app.post("/api/memory")
def save_memory(
    request: MemoryRequest,
):
    """
    Manually save a Memory Weaving thread.
    """

    thread = create_memory_thread(
        officer_id=request.officer_id,
        query=request.query,
        response=request.response,
        outcome=request.outcome,
        session_id=request.session_id,
    )

    return {
        "success": True,
        **thread,
    }


# ---------------------------------------------------------------------------
# GET /api/memory/{officer_id}
# ---------------------------------------------------------------------------

@app.get("/api/memory/{officer_id}")
def get_memory(
    officer_id: str,
    session_id: Optional[str] = Query(
        default=None
    ),
):
    """
    Retrieve Memory Weaving threads for an officer.
    """

    threads = get_memory_threads(
        officer_id=officer_id,
        session_id=session_id,
    )

    return {
        "officer_id": officer_id,
        "session_id": session_id,
        "threads": threads,
        "count": len(
            threads
        ),
    }


# ---------------------------------------------------------------------------
# GET /api/memory/{officer_id}/summary
# ---------------------------------------------------------------------------

@app.get(
    "/api/memory/{officer_id}/summary"
)
def get_memory_summary_api(
    officer_id: str,
):
    """
    Return memory analytics for an officer.
    """

    return get_memory_summary(
        officer_id
    )


# ---------------------------------------------------------------------------
# GET /api/memory/thread/{thread_id}
# ---------------------------------------------------------------------------

@app.get(
    "/api/memory/thread/{thread_id}"
)
def get_memory_thread_api(
    thread_id: str,
):
    """
    Return one Memory Weaving thread.
    """

    thread = get_memory_thread(
        thread_id
    )

    if thread is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Memory thread '{thread_id}' was not found."
            ),
        )

    return thread


# ---------------------------------------------------------------------------
# POST /api/memory/dissent
# ---------------------------------------------------------------------------

@app.post("/api/memory/dissent")
def save_dissent(
    request: DissentRequest,
):
    """
    Save investigator disagreement/agreement with an AI finding.

    This supports the Intelligence Brief dissent feedback mechanism.
    """

    thread = record_dissent(
        officer_id=request.officer_id,
        session_id=request.session_id,
        query=request.query,
        response=request.response,
        dissent=request.dissent,
        note=request.note,
    )

    return {
        "success": True,
        "message": (
            "Investigator feedback has been recorded "
            "in the Memory Weaving system."
        ),
        "memory_thread_id": (
            thread[
                "memory_thread_id"
            ]
        ),
        "thread": thread,
    }


# ---------------------------------------------------------------------------
# GET /api/alerts
# ---------------------------------------------------------------------------

@app.get("/api/alerts")
def get_alerts():
    """
    Return active crime pressure anomaly alerts.

    Alerts are generated dynamically from current pressure scores.
    """

    dynamic_alerts = generate_pressure_alerts(
        threshold=0.70
    )

    existing_alerts = get_active_alerts()

    # Merge alerts by zone.
    merged = {}

    for alert in existing_alerts:
        merged[
            alert["zone_id"]
        ] = alert

    for alert in dynamic_alerts:
        merged[
            alert["zone_id"]
        ] = alert

    alerts = list(
        merged.values()
    )

    return {
        "alerts": alerts,
        "count": len(
            alerts
        ),
        "anomaly_threshold": 0.70,
    }


# ---------------------------------------------------------------------------
# GET /api/alerts/count
# ---------------------------------------------------------------------------

@app.get("/api/alerts/count")
def get_alert_count():
    """
    Return a lightweight alert count for the frontend notification badge.
    """

    alerts = generate_pressure_alerts(
        threshold=0.70
    )

    return {
        "count": len(
            alerts
        ),
        "has_active_alerts": bool(
            alerts
        ),
    }


# ---------------------------------------------------------------------------
# SERVER ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
