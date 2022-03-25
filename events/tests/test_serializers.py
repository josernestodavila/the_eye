from datetime import datetime, timedelta
from unittest import TestCase
from uuid import uuid4

from django.utils import timezone

from events.models import Application, Event, Session
from events.serializers import EventSerializer


class EventSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.application = Application.objects.create(name='Test Application')

    def tearDown(self) -> None:

        Event.objects.all().delete()
        Session.objects.all().delete()
        Application.objects.all().delete()

    def test_serializer_creates_session_if_it_does_not_exist(self):

        self.assertFalse(Session.objects.exists())

        data = {
            "session_id": str(uuid4()),
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

        serializer = EventSerializer(
            data=data, context={"application_id": self.application.id}
        )

        self.assertTrue(serializer.is_valid())
        self.assertTrue(Session.objects.exists())

    def test_serializer_does_not_create_session_if_it_exists(self):

        session = Session.objects.create(application=self.application)
        data = {
            "session_id": session.id,
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

        serializer = EventSerializer(
            data=data, context={"application_id": self.application.id}
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(Session.objects.count(), 1)

    def test_serializer_is_not_valid_with_timestamp_future_dated(self):

        data = {
            "session_id": str(uuid4()),
            "category": "page interaction",
            "name": "pageview",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
            },
            "timestamp": timezone.localtime() + timedelta(hours=1),
        }

        serializer = EventSerializer(
            data=data, context={"application_id": self.application.id}
        )

        self.assertFalse(serializer.is_valid())

    def test_valid_serializer_creates_event(self):

        self.assertFalse(Event.objects.all().exists())

        data = {
            "session_id": str(uuid4()),
            "category": "page interaction",
            "name": "pageview",
            "data": {
                "host": "www.consumeraffairs.com",
                "path": "/",
            },
            "timestamp": timezone.make_aware(
                datetime.fromisoformat("2022-03-25 09:15:27.243860")
            ),
        }

        serializer = EventSerializer(
            data=data, context={"application_id": self.application.id}
        )
        self.assertTrue(serializer.is_valid())

        event = serializer.save()
        self.assertIsNotNone(event)
        self.assertTrue(Event.objects.all().exists())
