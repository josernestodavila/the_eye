from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from events.models import Application
from events.views import EventsView


class EventViewTestCase(TestCase):
    def setUp(self) -> None:

        self.application = Application.objects.create(name='Client 1')
        self.request_factory = APIRequestFactory()
        self.view = EventsView.as_view()

    def tearDown(self) -> None:
        self.application.delete()

    def test_unauthenticated_post_request_return_forbidden_response(self):

        request = self.request_factory.post(
            reverse('events'),
            data={
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "cta click",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/",
                    "element": "chat bubble",
                },
                "timestamp": "2021-01-01 09:15:27.243860",
            },
            format="json",
        )
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_get_request_return_forbidden_response(self):

        request = self.request_factory.get(reverse('events'))
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_post_with_invalid_payload_returns_bad_request_response(self):
        request = self.request_factory.post(
            reverse('events'),
            data={
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "cta click",
                "timestamp": "2021-01-01 09:15:27.243860",
            },
            format="json",
        )
        force_authenticate(request, user=self.application)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_get_request_return_ok_response(self):

        request = self.request_factory.get(reverse('events'))
        force_authenticate(request, user=self.application)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_with_valid_event_data_returns_no_content_response(self):

        request = self.request_factory.post(
            reverse('events'),
            data={
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "cta click",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/",
                    "element": "chat bubble",
                },
                "timestamp": "2021-01-01 09:15:27.243860",
            },
            format="json",
        )
        force_authenticate(request, user=self.application)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
