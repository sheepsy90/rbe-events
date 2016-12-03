from __future__ import unicode_literals

from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import User
from django.db import models

LOCATIONS = [
    ('offline', 'Offline'),
    ('online', 'Online')
]

PARTICIPATION_STATES = [
    ('interested', 'Interested'),
    ('going', 'Going'),
    ('not_going', 'Not going')
]

class Event(models.Model):
    creator = models.ForeignKey(User, help_text="The user creating the event and therefore able to edit it")
    title = models.CharField(max_length=128, help_text="A short name describing the Event")
    description = models.TextField()

    begin_time = models.DateTimeField(help_text="The time when the event begins - including timezone")
    end_time = models.DateTimeField(null=True)

    language = models.CharField(max_length=8, choices=LANGUAGES, help_text="The primary language that the event will be held in")

    medium = models.CharField(default="online", max_length=8, choices=LOCATIONS, help_text="Whether the event will be held online or offline")

    @property
    def display_language(self):
        return dict(LANGUAGES)[self.language]

    def __str__(self):
        return "{} // {} // {}".format(self.creator, self.title, self.begin_time.isoformat())

class EventParticipant(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    state = models.CharField(max_length=32, choices=PARTICIPATION_STATES)

    @property
    def display_state(self):
        return dict(PARTICIPATION_STATES)[self.state]