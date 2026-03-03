from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./finbot.db"
engine       = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base         = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"
    id          = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount      = Column(Float)
    category    = Column(String)
    date        = Column(String)
    created_at  = Column(DateTime, default=datetime.utcnow)


class ChatHistory(Base):
    __tablename__ = "chat_history"
    id         = Column(Integer, primary_key=True, index=True)
    role       = Column(String)
    message    = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_session():
    return SessionLocal()


def create_tables():
    Base.metadata.create_all(bind=engine)
