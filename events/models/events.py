from email.policy import default
from sqlite3 import Timestamp
from tabnanny import verbose
from unicodedata import category
from django.db import models


class Session(models.Model):
    id = models.UUIDField(primary_key=True)
    application = models.ForeignKey(
        to='events.Application',
        on_delete=models.CASCADE,
    )


class Event(models.Model):
    session = models.ForeignKey(to=Session, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    data = models.JSONField(default=dict)
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        indexes = [
            models.Index(fields=['timestamp'], name='timestamp_index'),
            models.Index(fields=['session', 'timestamp'], name='session_timestamp_index'),
        ]
        ordering = 'session', 'timestamp',
    
    def __str__(self) -> str:
        return f"Event {self.category} - {self.name}"
