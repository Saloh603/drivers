from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# --- ENUMS ---
class UserRole(str, enum.Enum):
    DRIVER = "driver"
    PASSENGER = "passenger"

class MatchStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

# --- MODELS ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    driver = relationship("Driver", back_populates="user", uselist=False)
    passenger = relationship("Passenger", back_populates="user", uselist=False)

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    car_model = Column(String, nullable=True)
    seats_available = Column(Integer, nullable=False)
    from_location = Column(String, nullable=False)
    to_location = Column(String, nullable=False)
    trip_time = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="driver")
    matches = relationship("Match", back_populates="driver")

class Passenger(Base):
    __tablename__ = "passengers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    people_count = Column(Integer, nullable=False)
    from_location = Column(String, nullable=False)
    to_location = Column(String, nullable=False)
    trip_time = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="passenger")
    matches = relationship("Match", back_populates="passenger")

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("passengers.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    status = Column(Enum(MatchStatus), default=MatchStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    passenger = relationship("Passenger", back_populates="matches")
    driver = relationship("Driver", back_populates="matches")
