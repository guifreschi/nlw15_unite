import pytest
from src.models.settings.connection import db_connection_handler
from .events_repository import EventsRepository

db_connection_handler.connect_to_db()

@pytest.mark.skip(reason="Novo registro em Banco de Dados.")
def test_insert_events():
    event = {
        "uuid": "meu-uuid",
        "title": "meu title",
        "slug": "Meu Slog Aqui",
        "maximum_attendees": 20
    }

    events_repository = EventsRepository()
    response = events_repository.insert_event(event)
    print(response)

# @pytest.mark.skip(reason="Não necessita.")
def test_get_event_by_id():
    event_id = 'meu-uuid-12312'

    events_repository = EventsRepository()
    response = events_repository.get_event_by_id(event_id)

    print(response)
