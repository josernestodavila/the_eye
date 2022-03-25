from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EventSerializer
from .models import Event
from .tasks import handle_event


class EventsView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter("session_id", OpenApiTypes.UUID, OpenApiParameter.QUERY),
            OpenApiParameter("category", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter(
                "timestamp_before", OpenApiTypes.DATETIME, OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                "timestamp_after", OpenApiTypes.DATETIME, OpenApiParameter.QUERY
            ),
        ],
    )
    def get(self, request):
        lookups = {}
        params = request.query_params.copy()

        if session_id := params.get("session_id"):
            lookups["session_id"] = session_id

        if category := params.get("category"):
            lookups["category"] = category

        if before := params.get("timestamp_before"):
            lookups["timestamp__lt"] = before

        if after := params.get("timestamp_after"):
            lookups["timestamp__gte"] = after

        events = Event.objects.filter(**lookups)

        serializer = self.serializer_class(events, many=True, read_only=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        application_id = request.user.id
        serializer = self.serializer_class(
            data=data, context={"application_id": application_id}
        )

        if serializer.is_valid():
            handle_event.delay(application_id, data)

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
