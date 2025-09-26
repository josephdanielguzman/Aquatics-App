from .db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
#stores models which create database tables

class Guards(Base):
    __tablename__ = "guards"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

class Breaks(Base):
    __tablename__ = "breaks"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)
    start_time = Column(String, nullable=True)
    end_time = Column(String, nullable=True)

    guard_id = Column(Integer, ForeignKey("guards.id", ondelete="CASCADE"), nullable=False)

class Spots(Base):
    __tablename__ = "spots"

    id = Column(Integer, primary_key=True, nullable=False)
    rotation_id = Column(Integer, ForeignKey("rotations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

class Shifts(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, nullable=False)
    guard_id = Column(Integer, ForeignKey("guards.id", ondelete="CASCADE"), nullable=False)
    started_at = Column(String, nullable=False)
    ended_at = Column(String, nullable=True)

class Rotations(Base):
    __tablename__ = "rotations"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)