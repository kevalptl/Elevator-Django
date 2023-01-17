**<h2>Elevator-Django**</h2>
**<h3>Steps to be followed for deployement</h3>**<br>
1) Make virtual environment venv in python3.7<br><br>
2) Install requirements.txt file in activated venv using<br> ```pip install -r requirements.txt```<br><br>
3) Make .env file inside elevatorproject/ directory
![Getting Started](image.png)
4) Perform migration of data into DB<br>
```python manage.py makemigrations```
```python manage.py migrate```<br><br>
5) Run Django app using command<br>
`python manage.py runserver`

