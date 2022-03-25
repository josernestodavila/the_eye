from events.models import Event, Session
from the_eye.celery import celery_app


@celery_app.task(name='handle_event')
def handle_event(application_id: int, payload: dict):
    session = Session.objects.filter(
        application_id=application_id,
        id=payload.get('session_id'),
    ).first()

    if not session:
        Session.objects.create(
            application_id=application_id,
            id=payload.get('session_id')
        )

    Event.objects.create(
        **payload
    )
