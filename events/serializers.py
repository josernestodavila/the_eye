from django.utils import timezone
from rest_framework import serializers

from events.models import Event, Session


class EventSerializer(serializers.ModelSerializer):

    session_id = serializers.UUIDField(required=True)
    category = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    data = serializers.JSONField(required=True)
    timestamp = serializers.DateTimeField(required=True)

    class Meta:
        model = Event
        fields = (
            "session_id",
            "category",
            "name",
            "data",
            "timestamp",
        )

    def validate_session_id(self, session_id):
        session = Session.objects.filter(
            id=session_id,
        ).first()

        if not session:
            Session.objects.create(
                id=session_id, application_id=self.context.get("application_id")
            )

        return session_id

    def validate_timestamp(self, timestamp):
        if timestamp > timezone.localtime():
            raise serializers.ValidationError(
                "Event timestamp cannot be dated in the future."
            )

        return timestamp
