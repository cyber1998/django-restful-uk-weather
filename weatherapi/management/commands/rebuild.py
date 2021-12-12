# Add flush command
# Nested iteration for each location and metrics
# save to database

import requests
from django.core.management import call_command
from django.core.management.base import BaseCommand
import io
import csv
import pandas as pd

from ...models import Location, Metric, Weather


class Command(BaseCommand):
 
    def get_data(self, url):
        response = requests.get(url).content.decode('ascii')
        f = io.StringIO(response)
        rows = []
        for i, line in enumerate(f.readlines()):
            if i >= 5:
                rows.append(line.split())
        
        f = io.StringIO()
        writer = csv.writer(f, delimiter=",")
        writer.writerows(rows)
        f.seek(0)

        df = pd.read_csv(f)
        return df


    @staticmethod
    def seed_locations():
        """
        This function will pre-populate the location table.

        :return:
        """
        names = ['UK', 'Scotland', 'Wales', 'England']
        for location in names:
            loc = Location(name=location)
            loc.save()

    @staticmethod
    def seed_metrics():
        """
        This function will pre-populate the metric table.
        :return:
        """
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

        month_to_MM = {
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr': 4,
            'may': 5,
            'jun': 6,
            'jul': 7,
            'aug': 8,
            'sep': 9,
            'oct': 10,
            'nov': 11,
            'dec': 12,
        }
       

        instances = []
        for location in locations:
            for metric in metrics:
                url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{metric.name}/date/{location.name}.txt"
                results = self.get_data(url)
                for _, value in results.iterrows():
                    year = value['year']
                    for month in results.columns[1:13]:
                        mm = month_to_MM[month]
                        try:
                            float(value[month])
                            instances.append(
                                Weather(
                                    measured_at='{}-{}-01'.format(year, mm),
                                    value=float(value[month]),
                                    metric=metric,
                                    location=location
                                )
                            )
                        except ValueError as e:
                            pass
                        
        self.stdout.write(
            self.style.SUCCESS('Successfully migrated all weather data'))
        Weather.objects.bulk_create(instances)
