from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from db.db import Base

class auth(Base):
    __tablename__ = "auth"

    auth_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, unique=True,  nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
