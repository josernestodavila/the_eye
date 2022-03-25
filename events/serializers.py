from rest_framework import serializers

from events.models import Event, Session


class EventSerializer(serializers.ModelSerializer):

    session_id = serializers.UUIDField()

    class Meta:
        model = Event
        fields = 'session_id', 'category', 'name', 'data', 'timestamp',

    def validate_session_id(self, session_id):
        session = Session.objects.filter(
            id=session_id,
        ).first()

        if not session:
            Session.objects.create(
                id=session_id,
                application_id=self.context.get('application_id')
            )

        return session_id

