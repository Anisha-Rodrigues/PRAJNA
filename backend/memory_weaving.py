"""
PRAJNA — Memory Weaving Engine
==============================

Stores investigator interactions as structured memory threads.

The current implementation uses in-memory storage so the application
works immediately without an external database.

The interface is deliberately separated from FastAPI so it can later
be replaced with Zoho Catalyst Data Store or another persistent store.
"""

from copy import deepcopy
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict, List, Optional
from uuid import uuid4


_MEMORY_THREADS: List[Dict[str, Any]] = []

_MEMORY_LOCK = Lock()


def _utc_timestamp():
    """
    Return an ISO-8601 UTC timestamp.
    """

    return datetime.now(
        timezone.utc
    ).isoformat()


def _generate_thread_id():
    """
    Generate a unique memory thread ID.
    """

    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%d%H%M%S"
    )

    unique_part = uuid4().hex[:8].upper()

    return f"MEM-{timestamp}-{unique_part}"


def classify_outcome(
    answer: str,
    cited_firs: Optional[List[str]] = None,
    nodes: Optional[List[Dict[str, Any]]] = None,
):
    """
    Automatically classify the outcome of a query.
    """

    cited_firs = cited_firs or []
    nodes = nodes or []

    if cited_firs or nodes:
        return "relevant_intelligence_found"

    answer_lower = (
        answer or ""
    ).lower()

    if (
        "no matching" in answer_lower
        or "no match" in answer_lower
    ):
        return "no_match"

    return "informational"


def create_memory_thread(
    officer_id: str,
    query: str,
    response: Dict[str, Any],
    outcome: str = "unclassified",
    session_id: Optional[str] = None,
):
    """
    Create and store a memory thread.
    """

    if not outcome or outcome == "unclassified":
        outcome = classify_outcome(
            response.get(
                "answer",
                "",
            ),
            response.get(
                "cited_firs",
                [],
            ),
            response.get(
                "nodes",
                [],
            ),
        )

    thread = {
        "memory_thread_id": _generate_thread_id(),
        "officer_id": officer_id,
        "session_id": session_id,
        "query": query,
        "response": deepcopy(response),
        "outcome": outcome,
        "timestamp": _utc_timestamp(),
    }

    with _MEMORY_LOCK:
        _MEMORY_THREADS.append(
            thread
        )

    return deepcopy(thread)


def get_memory_threads(
    officer_id: str,
    session_id: Optional[str] = None,
):
    """
    Retrieve memory threads for an officer.

    If session_id is supplied, only threads from that session are returned.
    """

    with _MEMORY_LOCK:

        threads = [
            thread
            for thread in _MEMORY_THREADS
            if thread["officer_id"] == officer_id
        ]

        if session_id:
            threads = [
                thread
                for thread in threads
                if thread.get("session_id") == session_id
            ]

        return deepcopy(
            list(
                reversed(threads)
            )
        )


def get_memory_thread(
    thread_id: str,
):
    """
    Retrieve one memory thread by ID.
    """

    with _MEMORY_LOCK:

        for thread in _MEMORY_THREADS:

            if (
                thread["memory_thread_id"]
                == thread_id
            ):
                return deepcopy(
                    thread
                )

    return None


def record_dissent(
    officer_id: str,
    session_id: Optional[str],
    query: str,
    response: Dict[str, Any],
    dissent: bool,
    note: str = "",
):
    """
    Record an investigator's disagreement with AI findings.

    This creates a dedicated memory thread so that human feedback
    becomes part of the Memory Weaving system.
    """

    dissent_response = {
        "type": "dissent_feedback",
        "dissent": dissent,
        "note": note,
        "original_response": deepcopy(
            response
        ),
    }

    outcome = (
        "officer_dissent"
        if dissent
        else "officer_agrees"
    )

    return create_memory_thread(
        officer_id=officer_id,
        query=query,
        response=dissent_response,
        outcome=outcome,
        session_id=session_id,
    )


def get_memory_summary(
    officer_id: str,
):
    """
    Return a summary of an officer's memory history.
    """

    threads = get_memory_threads(
        officer_id
    )

    outcome_counts = {}

    for thread in threads:

        outcome = thread.get(
            "outcome",
            "unclassified",
        )

        outcome_counts[outcome] = (
            outcome_counts.get(
                outcome,
                0,
            )
            + 1
        )

    return {
        "officer_id": officer_id,
        "total_threads": len(
            threads
        ),
        "outcome_counts": outcome_counts,
        "latest_thread": (
            threads[0]
            if threads
            else None
        ),
    }


def clear_memory():
    """
    Clear all in-memory threads.

    Useful for development and testing.
    """

    with _MEMORY_LOCK:
        _MEMORY_THREADS.clear()