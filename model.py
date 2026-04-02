from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from database import Base

import datetime


class ActivityLog(Base):
        __tablename__ = "activity_logs"
        id = Column(Integer, primary_key=True, index=True)
        timestamp = Column(DateTime, default=datetime.datetime.utcnow)
        activity_type = Column(String, nullable=False)
        site_name = Column(String, nullable=True)
        duration_minutes = Column(Float, nullable=False)
        completed = Column(Boolean, default=False)
        notes = Column(String, nullable=True)

        def __repr__(self):
                return f"<ActivityLog(id={self.id}, type={self.activity_type}, duration={self.duration_minutes}min)>"


class PomodoroSession(Base):
    __tablename__ = "pomodoro_sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_type = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<PomodoroSession(id={self.id}, type={self.session_type}, completed={self.completed})>"
