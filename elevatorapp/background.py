from background_task import background
import time
# from django.contrib.auth.models import User

@background()
def elevator_task(elevator_no):
    ##---------logic---------
    # while True
        # check if elevator is under maintainence is yes then open the door and break the loop
        # fetch moving status
        # if current floor==max floor or current floor==min floor  then
            # assign moving status stopped 
        # if moving status is up
    '''query for next destination floor matching 
    WHERE destination_floor > current_floor
    ORDER BY destination_floor ascending
    LIMIT 1'''
        # elif moving status is down 
    '''query for next destination floor matching 
    WHERE destination_floor > current_floor 
    ORDER BY destination_floor descending
    LIMIT 1'''
        # else
    '''query for next destination floor matching
    ORDER BY id ascending
    LIMIT 1'''
        # assign destination floor to the matched query if query exist else null
        # if door is closed
            # add the moving direction with current floor and intitalize current floor
            # update current floor 
    '''extract the query matching 
    WHERE current_floor = destination_floor'''
            # if query exist
                # open door for 3 sec and then close the door
                # delete all the query matched
    print("start")
    time.sleep(50)
    print("stopped")