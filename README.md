# Farely-server
Server to handle the backend service for Farely application

## How to Run
1. `pip install -r requirements.txt` (only on the first time or whenever the `requirements.txt` is updated)
2. `python manage.py collectstatic` (only on the first time or whenever the static files change)
3. `python manage.py runserver`

## How to Run Tests
1. `./manage.py test`

## Deployment Links
- Find Routes: https://rtkleong10-farely-server.herokuapp.com/api/find-routes/
- Calculate Fare: https://rtkleong10-farely-server.herokuapp.com/api/calculate-fare/
- Dummy Find Routes: https://rtkleong10-farely-server.herokuapp.com/api/dummy-find-routes/