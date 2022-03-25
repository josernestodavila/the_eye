import uuid

from django.db import models
from django.utils import timezone


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    application = models.ForeignKey(
        to="events.Application",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    def __str__(self) -> str:
        return f"Session {self.id} - {self.application.name}"


class Event(models.Model):
    session = models.ForeignKey(to=Session, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    data = models.JSONField(default=dict)
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        constraints = [
            models.CheckConstraint(
                check=models.Q(timestamp__lte=timezone.localtime()),
                name="event_timestamp_cannot_be_future_dated",
            )
        ]
        indexes = [
            models.Index(fields=["timestamp"], name="timestamp_index"),
            models.Index(
                fields=["session", "timestamp"], name="session_timestamp_index"
            ),
        ]
        ordering = (
            "session",
            "timestamp",
        )

    def __str__(self) -> str:
        return f"Event {self.category} - {self.name}"
