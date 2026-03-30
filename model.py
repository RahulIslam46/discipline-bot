from sqlalchemy import Column, Integer, String,DateTime,Boolean,Float
from database import Base

import datetime

class ActivityLog(Base):
     __tablename__ = "activity_log"
     id=Column(Integer,primary_key=True,index=True)
     timestamp=Column(DateTime,default=datetime.datetime.utcnow)
     activity_type=Column(String)
     site_name=Column(String)
     duration_minuts=Column(Float)
     completed=Column(Boolean,default=False)
     notes=Column(String,nullable=True)
     def __repr__(self):
        return f"<ActivityLog(id={self.id}, type={self.activity_type}, duration={self.duration_minutes}min)>"

class PromodoroSession(Base):
        __tablename__ = "promodoro_sessions"
        id=Column(Integer,primary_key=True,index=True)
        start_time=Column(DateTime,default=datetime.datetime.utcnow)
        end_time=Column(DateTime,nullable=True)
        session_type=Column(String)
        compileted=Column(Boolean,default=False)
        interruptions=Column(Integer,default=0)
        def __repr__(self):
            return f"<PomodoroSession(id={self.id}, type={self.session_type}, completed={self.completed})>"
class Blocksite(Base):
     __tablename__ ="blocked_sites"
     id = Column(Integer,primary_key=True,index=True)
     site_url=Column(String,unique=True)
     blocked_at=Column(DateTime,default=datetime.datetime.utcnow)
     block_counter=Column(Integer,default=0)
     is_active=Column(Boolean,default=True)
     def __repr__(self):
                 return f"<BlockedSite(site={self.site_url}, active={self.is_active})>"     
