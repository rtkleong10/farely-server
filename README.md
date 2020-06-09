# Farely-server
Server to handle the backend service for Farely Android application. The Android application was developed separately This is a school project I did for CZ2006 Software Engineering. My group mates are Chulpaibul Jiraporn, Nguyen Duy Khanh, Rachel Khan, Tran Anh Tai and Truong Quang Duc. The documentation is available at https://rtkleong10.github.io/farely-server/.

## How to Run
1. `pip install -r requirements.txt`
2. `python manage.py runserver`
3. Open [http://127.0.0.1:8000/api/find-routes/](http://127.0.0.1:8000/api/find-routes/) in a web browser

### Prerequisites
- Installed [Python](https://www.python.org/)

## How to Generate Documentation
1. `pdoc --html --force farely_api`
2. Documentation generated in the `html/` folder
3. Transfer files in the `html/farely_api` folder to the `docs/` folder

## How to Run Tests
1. `python manage.py test`

### Note
- Tests are incomplete as it was removed from the project deliverables