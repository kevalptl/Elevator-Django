from background_task import background
import time
# from django.contrib.auth.models import User

@background()
def elevator_system(elevator_no):
    print("start")
    time.sleep(50)
    print("stopped")