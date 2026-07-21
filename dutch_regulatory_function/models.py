from sqlalchemy import Column, Integer, String, DateTime 
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Publication(Base):
    __tablename__ = 'publications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String, nullable=False)
    guid = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    description = Column(String, nullable=True)
    pub_date = Column(DateTime(timezone=True), nullable=True) 
    language = Column(String, nullable=False) 
    fetched_at = Column(DateTime(timezone=True), nullable=False)
