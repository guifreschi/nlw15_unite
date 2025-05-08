from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.models.settings.base import Base

class CheckIns(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now()) # pylint: disable=not-callable
    attendeeId = Column(String, ForeignKey("attendees.id"))

    def __repr__(self):
        return f"CheckIns [attendeeId={self.attendeeId}]"
