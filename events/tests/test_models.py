from datetime import timedelta, datetime
from unittest import TestCase

from django.db import IntegrityError
from django.utils import timezone

from events.models import Application, Event, Session


class ApplicationTestCase(TestCase):
    def tearDown(self) -> None:
        Application.objects.all().delete()

    def test_application_created_successfully(self):

        application = Application.objects.create(name='iOS Client')

        self.assertIsNotNone(application)

    def test_create_application_with_same_name_raises_exception(self):

        Application.objects.create(name='Web Client')

        with self.assertRaises(IntegrityError):
            Application.objects.create(name='Web Client')


class SessionTestCase(TestCase):
    def setUp(self) -> None:
        self.application = Application.objects.create(name='Testing Application')

    def tearDown(self) -> None:
        self.application.delete()

    def test_session_created_successfully(self):

        session = Session.objects.create(application=self.application)

        self.assertIsNotNone(session)

    def test_create_session_with_duplicated_id_raises_exception(self):

        session = Session.objects.create(application=self.application)

        with self.assertRaises(IntegrityError):
            Session.objects.create(id=session.id, application=self.application)

    def test_create_session_with_duplicated_id_from_another_application_raises_exception(self):

        session = Session.objects.create(application=self.application)
        client_app = Application.objects.create(name='Another Client')

        with self.assertRaises(IntegrityError):
            Session.objects.create(id=session.id, application=client_app)


class EventTestCase(TestCase):
    def setUp(self) -> None:

        self.application = Application.objects.create(name='Client')
        self.session = Session.objects.create(application=self.application)

    def tearDown(self) -> None:

        Event.objects.all().delete()
        Session.objects.all().delete()
        Application.objects.all().delete()

    def test_event_created_successfully(self):

        data = {
            "session_id": self.session.id,
            "category": "page interaction",
            "name": "pageview",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
            },
            "timestamp": timezone.make_aware(
                datetime.fromisoformat("2021-01-01 09:15:27.243860")
            ),
        }
        event = Event.objects.create(**data)

        self.assertIsNotNone(event)
        self.assertTrue(Event.objects.filter(session_id=self.session.id).exists())

    def test_create_event_with_future_dated_timestamp_raises_exception(self):

        data = {
            "session_id": self.session.id,
            "category": "page interaction",
            "name": "pageview",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
            },
            "timestamp": timezone.localtime() + timedelta(hours=1),
        }

        with self.assertRaises(IntegrityError):
            Event.objects.create(**data)
