from db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Time

class Guards(Base):
    __tablename__ = "guards"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

class Breaks(Base):
    __tablename__ = "breaks"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(
        Integer,
        ForeignKey("break_types.id", ondelete="CASCADE"),
        nullable=False
    )
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=True)

    guard_id = Column(
        Integer,
        ForeignKey("guards.id", ondelete="CASCADE"),
        nullable=False
    )

class Spots(Base):
    __tablename__ = "spots"

    id = Column(Integer, primary_key=True, nullable=False)
    rotation_id = Column(
        Integer,
        ForeignKey("rotations.id", ondelete="CASCADE"),
        nullable=False
    )
    name = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

class Shifts(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, nullable=False)
    guard_id = Column(
        Integer,
        ForeignKey("guards.id", ondelete="CASCADE"),
        nullable=False
    )
    started_at = Column(Time, nullable=False)
    ended_at = Column(Time, nullable=True)

class Rotations(Base):
    __tablename__ = "rotations"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

class Assignments(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, nullable=False)
    shift_id = Column(
        Integer,
        ForeignKey("shifts.id", ondelete="CASCADE"),
        nullable=False
    )
    spot_id = Column(
        Integer,
        ForeignKey("spots.id", ondelete="CASCADE"),
        nullable=True
    )
    time = Column(Time, nullable=False)

class BreakTypes(Base):
    __tablename__ = "break_types"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)