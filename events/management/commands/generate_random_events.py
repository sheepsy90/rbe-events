import random

from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils import timezone

from events.models import Event, LOCATIONS


class Command(BaseCommand):
    help = 'Sets up a basic set of objects for testing purposes'

    def get_random_datetime(self):
        day = random.randint(1, 30)
        month = random.randint(1, 12)
        year = random.choice([2016])

        hour = random.randint(0, 23)
        minute = random.randint(0, 59)

        return timezone.datetime(day=day, month=month, year=year, hour=hour, minute=minute)


    def handle(self, *args, **options):
        user = User.objects.get(username='sheepsy90')

        for i in range(250):
            begin_time = self.get_random_datetime()
            e = Event(creator=user, title="Some event title longer event title in this case", description="Lorem ipsum "*28,
                      language=random.choice(LANGUAGES)[0], begin_time=begin_time, medium=random.choice(LOCATIONS)[0])
            e.save()
