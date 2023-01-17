from background_task import background
import time
from .models import *
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
    elevator = Elevator.objects.all()
    min_floor = elevator.values()[0]['min_floor']
    max_floor = elevator.values()[0]['max_floor']
    while True:
        elevator_car = ElevatorCar.objects.filter(elevator_no=elevator_no)
        if elevator_car.values()[0]['is_underMaintenance']:
            break
        moving_status = elevator_car.values()[0]['moving_status']
        current_floor = elevator_car.values()[0]['current_floor']
        print("moving_status:",moving_status)
        print("current_floor:",current_floor)
        if current_floor==min_floor or current_floor==max_floor:
            moving_status=0
        if moving_status==1:
            destination_query =  ElevatorRequest.objects.filter(elevator_no=elevator_no, destination_floor__gt=current_floor).order_by('destination_floor')
        elif moving_status==-1:
            destination_query =  ElevatorRequest.objects.filter(elevator_no=elevator_no, destination_floor__lt=current_floor).order_by('-destination_floor')
        else:
            destination_query =  ElevatorRequest.objects.filter(elevator_no=elevator_no).order_by('id')
        print("destination_query:",destination_query)
        destination_floor = destination_query.values()[0]['destination_floor'] if destination_query else None
        print("destination_floor:",destination_floor)
        if destination_floor==None:
            ElevatorCar.objects.filter(elevator_no=elevator_no).update(moving_status=0)
            ElevatorCar.objects.filter(elevator_no=elevator_no).update(destination_floor=destination_floor)
            break
        if moving_status==0:
            moving_status = 1 if destination_floor>current_floor else -1 if destination_floor<current_floor else 0
        ElevatorCar.objects.filter(elevator_no=elevator_no).update(moving_status=moving_status)
        ElevatorCar.objects.filter(elevator_no=elevator_no).update(destination_floor=destination_floor)
        if not elevator_car.values()[0]['is_doorOpen']:
            current_floor = current_floor + moving_status
            print("moving_status:",moving_status)
            print("current_floor:",current_floor)
            ElevatorCar.objects.filter(elevator_no=elevator_no).update(current_floor=current_floor)
            check_destination_query = ElevatorRequest.objects.filter(elevator_no=elevator_no, destination_floor=current_floor)
            if check_destination_query:
                print("check_query:",check_destination_query)
                ElevatorCar.objects.filter(elevator_no=elevator_no).update(is_doorOpen=True)
                print("door has opened")
                time.sleep(5)
                print("door has closed")
                ElevatorCar.objects.filter(elevator_no=elevator_no).update(is_doorOpen=False)
                ElevatorRequest.objects.filter(elevator_no=elevator_no, destination_floor=current_floor).delete()
            else:
                print("No request found on floor no:",current_floor)
                time.sleep(1)
        else:
            print("door kept open")
            print("please close the door")
            time.sleep(1)
    print("DONE")



@background()
def door_task(elevator_no):
    ElevatorCar.objects.filter(elevator_no=elevator_no).update(is_doorOpen=True)
    print("door has open")
    time.sleep(5)
    ElevatorCar.objects.filter(elevator_no=elevator_no).update(is_doorOpen=False)
    print("door has closed")