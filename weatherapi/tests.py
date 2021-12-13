from django.test import TestCase
from rest_framework.test import RequestsClient
from django.test.utils import override_settings


# Create your tests here.

@override_settings(DEBUG=True)
class WeatherTestCase(TestCase):

    fixtures = ['db_data']

    def test_get_weather(self):
        """
        This test determines if the GET requests are working properly.
        """

        client = RequestsClient()
        response = client.get(
            'http://localhost:8000/weather-report',
            params={
                'start_date': '2001-01-01',
                'end_date': '2010-01-01',
                'metric': 'Rainfall',
                'location': 'UK'
            }
        )
        assert response.status_code == 200

        #  Test for delivering the weather data

        assert response.json()[0] == {"2001-01": 79.4}
        assert response.json()[1] == {"2001-02": 97.1}
        assert response.json()[2] == {"2001-03": 85.7}

    def test_check_duplicate_data(self):
        """
        This test determines if there are any duplicate values in the
        data.
        """

        client = RequestsClient()
        response = client.get(
            'http://localhost:8000/weather-report',
            params={
                'start_date': '2001-01-01',
                'end_date': '2010-01-01',
                'metric': 'Rainfall',
                'location': 'Scotland'
            }
        )
        assert response.status_code == 200

        #  Test for checking for duplicate values

        test_object_list = []  # List to count the result
        for result in response.json():

            if result == {"2001-01": 91.6}:
                test_object_list.append(result)

        assert len(test_object_list) == 1

        response = client.get(
            'http://localhost:8000/weather-report',
            params={
                'start_date': '2001-01-01',
                'end_date': '2010-01-01',
                'metric': 'Tmax',
                'location': 'UK'
            }
        )
        assert response.status_code == 200

        #  Test for checking duplicate values

        test_object_list = []  # List to count the result
        for result in response.json():
            if result == {"2001-01": 5.3}:
                test_object_list.append(result)

        assert len(test_object_list) == 1
