"""SCAMEATER API - FastAPI internal REST API."""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import structlog

log = structlog.get_logger()

app = FastAPI(
    title="SCAMEATER API",
    description="Internal REST API for SCAMEATER honeypot system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydantic Models ---

class CallSummary(BaseModel):
    id: str
    caller_number: str
    started_at: datetime
    duration_seconds: Optional[int] = None
    persona_name: str
    scam_type: Optional[str] = None
    scam_confidence: Optional[float] = None
    analysis_status: str


class CallDetail(CallSummary):
    transcript_text: Optional[str] = None
    transcript_full: Optional[List[dict]] = None
    caller_country: Optional[str] = None
    caller_region: Optional[str] = None
    techniques_used: Optional[List[str]] = None
    cost_total: Optional[float] = None


class SystemStatus(BaseModel):
    status: str
    active_calls: int
    total_calls_today: int
    database_connected: bool
    redis_connected: bool


# --- Health Check ---

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.get("/status", response_model=SystemStatus)
async def get_status():
    """Get system status."""
    return SystemStatus(
        status="running",
        active_calls=0,
        total_calls_today=0,
        database_connected=True,
        redis_connected=True
    )


# --- Calls Endpoints ---

@app.get("/api/v1/calls", response_model=List[CallSummary])
async def list_calls(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    scam_type: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None
):
    """List all calls with optional filters."""
    # In production, this would query the database
    return []


@app.get("/api/v1/calls/{call_id}", response_model=CallDetail)
async def get_call(call_id: str):
    """Get detailed information about a specific call."""
    # In production, this would query the database
    raise HTTPException(status_code=404, detail="Call not found")


@app.delete("/api/v1/calls/{call_id}")
async def delete_call(call_id: str):
    """Delete a call and its associated audio/transcripts."""
    raise HTTPException(status_code=404, detail="Call not found")


# --- Stats Endpoints ---

@app.get("/api/v1/stats/overview")
async def get_stats_overview():
    """Get overview statistics."""
    return {
        "total_calls": 0,
        "total_duration_seconds": 0,
        "total_cost": 0.0,
        "calls_today": 0,
        "avg_duration_seconds": 0,
        "avg_cost": 0.0
    }


@app.get("/api/v1/stats/scams")
async def get_scams_stats():
    """Get scam type distribution."""
    return {}


# --- Blacklist Endpoints ---

@app.get("/api/v1/blacklist")
async def list_blacklist(limit: int = 100):
    """List blacklisted numbers."""
    return []


@app.post("/api/v1/blacklist")
async def add_to_blacklist(phone_number: str, scam_type: str, confidence: float):
    """Add a number to the blacklist."""
    return {"status": "added", "phone_number": phone_number}


# --- Export Endpoints ---

@app.get("/api/v1/export/calls")
async def export_calls(format: str = "json"):
    """Export calls data."""
    if format not in ["json", "csv"]:
        raise HTTPException(status_code=400, detail="Format must be json or csv")
    return {"data": [], "format": format}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
