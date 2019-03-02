# Add flush command
# Nested iteration for each location and metrics
# save to database

import requests
from django.core.management import call_command
from django.core.management.base import BaseCommand


from ...models import Location, Metric, Weather


class Command(BaseCommand):
    # help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    @staticmethod
    def seed_locations():
        names = ['UK', 'Scotland', 'Wales', 'England']
        for location in names:
            loc = Location(name=location)
            loc.save()

    @staticmethod
    def seed_metrics():
        names = ['Tmax', 'Tmin', 'Rainfall']
        for metric in names:
            locations = Location.objects.all()
            met = Metric(name=metric)
            met.save()
            for location in locations:
                met.locations.add(location)

    def handle(self, *args, **options):
        """
        This function is the main handler for this management command.
        Calling this command will seed the required tables with the
        appropriate data.

        :param args: Optional arguments passed to the command
        :param options: Optional options passed for any argument

        :return None:
        """
        self.stdout.write(
            self.style.SUCCESS('Building tables..'))
        call_command('flush')
        Command.seed_locations()
        Command.seed_metrics()

        locations = Location.objects.all()
        metrics = Metric.objects.all()

        url = 'https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/{}-{}.json'
        instances = []
        for location in locations:
            for m in metrics:
                results = requests.get(url.format(m.name, location.name))
                for result in results.json():
                    instances.append(
                        Weather(measured_at='{}-{}-01'.format(result['year'], result['month']),
                                             value=float(result['value']),
                                             # month=int(result['month']),
                                             metric=m,
                                             location=location))
        self.stdout.write(
            self.style.SUCCESS('Successfully migrated all weather data'))
        Weather.objects.bulk_create(instances)
