# Farely-server
Server to handle the backend service for Farely application

## How to Run
1. `pip install -r requirements.txt`
2. `python manage.py runserver`
3. Open [http://127.0.0.1:8000/api/find-routes/](http://127.0.0.1:8000/api/find-routes/) in a web browser

### Prerequisites
- Installed [Python](https://www.python.org/)

## How to Generate Documentation
1. `pdoc --html --force farely_api`
2. Documentation generated in the `html/` folder

## How to Run Tests
1. `python manage.py test`

### Note
- Tests are incomplete as it was removed from the project deliverables

## Deployment Links
- [Find Routes API](https://rtkleong10-farely-server.herokuapp.com/api/find-routes/)
- [Documentation](https://rtkleong10-farely-server.herokuapp.com/docs/)