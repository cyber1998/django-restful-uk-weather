# django-restful-uk-weather
A django restful app that presents weather data for UK from 1910 - 2017

Steps to run the application

1. Install all requirements by typing `pip install -r requirements.txt`

2. Build your migrations by typing `python manage.py makemigrations`

3. Migrate your data and create the tables by typing `pip manage.py migrate`

4. Populate the database by typing `pip manage.py rebuild`

5. Make a GET request to `/weather-report` using any of the following query parameters: <br>

    a. `start_date`: The start date in the format YYYY-MM-DD <br>
    a. `end_date`: The end date in the format YYYY-MM-DD <br>
    a. `metric`: Any of the currently available metrics [Rainfall, Tmax, Tmin] <br>
    a. `location`: Any of the currently available locations [UK, Scotland, Wales, England]<br>
    
6. Tests can be run with `python manage.py test`