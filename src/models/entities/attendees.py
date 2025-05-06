from src.models.settings.base import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, ForeignKey

class Attendees(Base):
    __tablename__ = "attendees"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    event_id = Column(String, ForeignKey("events.id"))
    created_at = Column(DateTime, default=func.now()) # pylint: disable=not-callable

    def __repr__(self):
        return f"Attendees [name={self.name}, email={self.email}, event_id={self.event_id}]"
