from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
            "ppmodoro": "/pomodoro",
            "blocker": "/blocker"
        }
    }        

