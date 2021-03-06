# Generated by Django 4.0.3 on 2022-03-25 18:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_alter_session_options_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="event",
            name="event_timestamp_cannot_be_future_dated",
        ),
        migrations.RemoveConstraint(
            model_name="session",
            name="unique_application_session",
        ),
        migrations.AlterField(
            model_name="session",
            name="id",
            field=models.UUIDField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AddConstraint(
            model_name="event",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "timestamp__lte",
                        datetime.datetime(2022, 3, 25, 18, 48, 59, 26836, tzinfo=utc),
                    )
                ),
                name="event_timestamp_cannot_be_future_dated",
            ),
        ),
    ]
