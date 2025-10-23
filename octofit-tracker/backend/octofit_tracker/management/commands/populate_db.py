from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):

        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Deleting old data...'))
            for obj in Activity.objects.all():
                if getattr(obj, 'id', None):
                    obj.delete()
            for obj in Workout.objects.all():
                if getattr(obj, 'id', None):
                    obj.delete()
            for obj in Leaderboard.objects.all():
                if getattr(obj, 'id', None):
                    obj.delete()
            for obj in User.objects.all():
                if getattr(obj, 'id', None):
                    obj.delete()
            for obj in Team.objects.all():
                if getattr(obj, 'id', None):
                    obj.delete()

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel = Team.objects.create(name='Marvel')
            dc = Team.objects.create(name='DC')

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            users = [
                User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
                User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
                User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
                User.objects.create(name='Batman', email='batman@dc.com', team=dc),
            ]

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            Activity.objects.create(user=users[0], type='Web Swing', duration=30)
            Activity.objects.create(user=users[1], type='Suit Up', duration=20)
            Activity.objects.create(user=users[2], type='Lasso Practice', duration=25)
            Activity.objects.create(user=users[3], type='Detective Work', duration=40)

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            w1 = Workout.objects.create(name='Hero Training', description='Intense superhero workout')
            w1.suggested_for.add(marvel, dc)

            self.stdout.write(self.style.SUCCESS('Creating leaderboards...'))
            Leaderboard.objects.create(team=marvel, points=100)
            Leaderboard.objects.create(team=dc, points=90)

            self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
