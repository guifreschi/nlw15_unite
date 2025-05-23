import uuid
from src.models.repository.attendees_repository import AttendeesRepository
from src.models.repository.events_repository import EventsRepository
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse

class AttendeesHandler:
    def __init__(self) -> None:
        self.__attendees_repository = AttendeesRepository()
        self.__events_repository = EventsRepository()

    def registry(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body
        event_id = http_request.param["event_id"]

        event_attendees_count = self.__events_repository.count_event_attendees(event_id)

        if (
            event_attendees_count["attendeesAmount"]
            and event_attendees_count["maximumAttendees"] < event_attendees_count["attendeesAmount"]
        ):
            raise Exception("Evento Lotado!")

        body["uuid"] = str(uuid.uuid4())
        body["event_id"] = event_id
        self.__attendees_repository.insert_attendee(body)

        return HttpResponse(body=None, status_code=201)

    def find_attendee_badge(self, http_request: HttpRequest) -> HttpResponse:
        attendee_id = http_request.param["attendee_id"]
        badge = self.__attendees_repository.get_attendee_badge_by_id(attendee_id)

        if not badge:
            raise Exception("Participante não encontrado!") 

        return HttpResponse(
            body={
                "badge": {
                    "name": badge.name,
                    "email": badge.email,
                    "event_title": badge.title
                }
            }, 
            status_code=200)
