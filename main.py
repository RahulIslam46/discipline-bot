from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from model import ActivityLog, PomodoroSession
import datetime
from typing import Optional, List

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Discipline Agent API",
    description="AI-powered API for tracking and managing user activities, promoting productivity and focus.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schemas ──────────────────────────────────────────────

class LogCreate(BaseModel):
    activity_type: str
    site_name: Optional[str] = None
    duration_minutes: float
    completed: bool = False
    notes: Optional[str] = None

class PomodoroCreate(BaseModel):
    session_type: str  # "work" or "break"

class ActivityResponse(BaseModel):
    id: int
    timestamp: datetime.datetime
    activity_type: str
    site_name: Optional[str] = None
    duration_minutes: float
    completed: bool

    class Config:
        from_attributes = True

class PomodoroResponse(BaseModel):
    id: int
    session_type: str
    completed: bool
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

# ── Root ─────────────────────────────────────────────────

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Discipline Agent API",
        "endpoints": {
            "docs": "/docs",
            "activity_logs": "/activity-logs",
            "pomodoro": "/pomodoro"
        }
    }

# ── Activity Log Endpoints ────────────────────────────────

@app.post("/activity-logs", response_model=ActivityResponse)
def create_activity_log(log: LogCreate, db: Session = Depends(get_db)):
    entry = ActivityLog(**log.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@app.get("/logs", response_model=List[ActivityResponse])
def get_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

@app.get("/logs/today", response_model=List[ActivityResponse])
def get_logs_today(db: Session = Depends(get_db)):
    today = datetime.date.today()
    logs = (
        db.query(ActivityLog)
        .filter(ActivityLog.timestamp >= datetime.datetime.combine(today, datetime.time.min))
        .order_by(ActivityLog.timestamp.desc())
        .all()
    )
    return logs

@app.delete("/logs/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(ActivityLog).filter(ActivityLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log entry not found")
    db.delete(log)
    db.commit()
    return {"message": "Log entry deleted successfully"}

# ── Pomodoro Endpoints ────────────────────────────────────

@app.post("/pomodoro", response_model=PomodoroResponse)
def create_pomodoro(data: PomodoroCreate, db: Session = Depends(get_db)):
    session = PomodoroSession(**data.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@app.patch("/pomodoro/{session_id}/complete", response_model=PomodoroResponse)
def complete_pomodoro(session_id: int, db: Session = Depends(get_db)):
    session = db.query(PomodoroSession).filter(PomodoroSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    setattr(session, "completed", True)
    setattr(session, "end_time", datetime.datetime.now(datetime.timezone.utc))
    db.commit()
    db.refresh(session)
    return session

@app.get("/pomodoro/stats")
def get_pomodoro_stats(db: Session = Depends(get_db)):
    total = db.query(PomodoroSession).count()
    completed = db.query(PomodoroSession).filter(PomodoroSession.completed == True).count()
    today = datetime.date.today()
    today_count = (
        db.query(PomodoroSession)
        .filter(PomodoroSession.start_time >= datetime.datetime.combine(today, datetime.time.min))
        .count()
    )
    return {
        "total_sessions": total,
        "completed_sessions": completed,
        "completion_rate": f"{(completed / total * 100):.1f}%" if total > 0 else "0%",
        "today_sessions": today_count
    }