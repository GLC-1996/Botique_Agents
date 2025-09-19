from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from common.models import Proposal

engine = create_engine("sqlite:///proposal_db.sqlite3")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ApprovedPlan(Base):
    __tablename__ = "approved_plans"
    id = Column(Integer, primary_key=True)
    approved_by = Column(String)
    approved_at = Column(DateTime)
    strategy_text = Column(String)
    cost_impact = Column(JSON)
    confidence = Column(Float)
    goal = Column(String)
    actions = Column(JSON)
    guardrails_applied = Column(JSON)
    meta = Column(JSON)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
