from typing import Dict
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from src.models.settings.connection import db_connection_handler
from src.models.entities.events import Events
from src.models.entities.attendees import Attendees

class EventsRepository:
    def insert_event(self, events_info: Dict) -> Dict:
        with db_connection_handler as database:
            try:
                event = Events(
                    id=events_info.get('uuid'),
                    title=events_info.get('title'),
                    details=events_info.get('details'),
                    slug=events_info.get('slug'),
                    maximum_attendees=events_info.get('maximum_attendees'),
                )
                database.session.add(event)
                database.session.commit()

                return events_info
            except IntegrityError:
                raise Exception("Evento já cadastrado!") # pylint: disable=raise-missing-from

            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_event_by_id(self, event_id: str) -> Events:
        with db_connection_handler as database:
            try:
                event = (
                    database.session
                    .query(Events)
                    .filter(Events.id==event_id)
                    .one()
                )
                return event
            except NoResultFound:
                return None

    def count_event_attendees(self, event_id) -> Dict:
        with db_connection_handler as database:
            event_count = (
                database.session
                .query(Events)
                .join(Attendees, Events.id == Attendees.event_id)
                .filter(Events.id == event_id)
                .with_entities(
                    Events.maximum_attendees,
                    Attendees.id
                )
                .all()
            )

            if len(event_count) == 0:
                return {
                    "maximumAttendees": 0,
                    "attendeesAmount": 0
                }

            return {
                    "maximumAttendees": event_count[0].maximum_attendees,
                    "attendeesAmount": len(event_count)
                }
