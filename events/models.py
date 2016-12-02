from __future__ import unicode_literals

from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import User
from django.db import models

LOCATIONS = [
    ('offline', 'Offline'),
    ('online', 'Online')
]


class Event(models.Model):
    creator = models.ForeignKey(User, help_text="The user creating the event and therefore able to edit it")
    title = models.CharField(max_length=128, help_text="A short name describing the Event")
    description = models.TextField()

    begin_time = models.DateTimeField(help_text="The time when the event begins - including timezone")
    end_time = models.DateTimeField(null=True)

    language = models.CharField(max_length=8, choices=LANGUAGES, help_text="The primary language that the event will be held in")

    medium = models.CharField(default="online", max_length=8, choices=LOCATIONS, help_text="Whether the event will be held online or offline")


class EventLocation(models.Model):
    latitude = models.CharField(max_length=32)
    longitude = models.CharField(max_length=32)
    description = models.CharField(max_length=256)