**<h2>Elevator-Django**</h2>
**<h3>Steps to be followed for deployement</h3>**
1) Create virtual environment venv in python3.7<br><br>
2) Install requirements.txt file in activated venv using<br> ```pip install -r requirements.txt```<br><br>
3) Make .env file inside *elevatorproject/* directory with following keys<br>
`SECRET_KEY="<django_secret_key>"`<br>
`DB_NAME="<db_name>"`<br>
`DB_USER="<username>"`<br>
`DB_PASSWORD="<password>"`<br>
`DB_HOST="<host>"`<br>
`DB_PORT="<port>"`<br><br>
4) Perform migration of data into DB<br>
```python manage.py makemigrations```<br>
```python manage.py migrate```<br><br>
5) Run django app using command<br>
`python manage.py runserver`<br><br>
6) To run elevator tasks in background<br>
`python manage.py process_tasks`<br><br>


**<h3>Why used background tasks?</h3>**
The elevator system process required to run continously to serves the requests recieved in real time from API. So I have used *django-background-tasks* which will continously keep check on database and state of an elevator such that it will do the apropriate changes on models data.

**<h3>Next steps to optimize</h3>**
* We can use redis (cache memory) to save and serve requests(instead of ElevatorRequest model) for an elevators.<br>
* Add authentication header in API

