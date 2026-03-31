from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from requests import session
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine,get_db
from model import ActivityLog, PromodoroSession, Blocksite
import datetime
from typing import Optional,List
    

Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="Descipline Agent API",
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

class LogCreate(BaseModel):
    activity_type:str
    site_name:Optional[str]=None
    duration_minutes:float
    completed:bool=False
    notes:Optional[str]=None

class PomodoroCreate(BaseModel):
    session_type:str
    completed:bool=False

class BlocksiteCreate(BaseModel):
    site_url:str        

class ActivityResponse(BaseModel):
    id:int 
    timestamp:datetime.datetime
    activity_type:str
    site_name:Optional[str]=None
    duration_minutes:float
    completed:bool

    class Config:
        from_attribute=True

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Descipline Agent API",
        "endpoints":{
            "docs": "/docs",
            "activity_logs": "/activity-logs",
            "pomodoro": "/pomodoro",
            "blocker": "/blocker"
        }
    }       
#Activity Log Endpoints
@app.post("/activity-logs", response_model=ActivityResponse)
def create_activity_log(log: LogCreate, db: Session = Depends(get_db)):
    entry= ActivityLog(**log.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get('/logs', response_model=List[ActivityResponse])
def get_logs(skip: int = 0,limit:int =100,db:Session=Depends(get_db)):
    logs=db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

@app.get('/logs/today', response_model=List[ActivityResponse])
def get_logs_today(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    today = datetime.date.today()
    logs = db.query(ActivityLog).filter(ActivityLog.timestamp >= today).order_by(ActivityLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

@app.delete('/logs/{log_id}')
def delete_log(log_id: int, db: Session = Depends(get_db)):
    log = db.query(ActivityLog).filter(ActivityLog.id == log_id).first()
    if not log:
        return {"error": "Log entry not found"}
    db.delete(log)
    db.commit()
    return {"message": "Log entry deleted successfully"}

@app.post('/pomodoro')
def create_promodoro(session:PromodoroSession,db:Session = Depends(get_db)):
    promodoro=PromodoroSession(**session.dict())
    db.add(promodoro)
    db.commit()
    db.refresh(promodoro)
    return {"message":"Pomodoro session created successfully", "session_id": promodoro.id}
