from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .background import elevator_task
from background_task.models import Task
from .models import *

@csrf_exempt
def init_elevator(request):
    response_data={}
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        try:
            request = json.loads(body_unicode)
        except:
            response_data['message']="request body format is incorrect"
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
        no_of_elevator = request.get('no_of_elevator')
        min_floor = request.get('min_floor')
        max_floor = request.get('max_floor')
        missing_req_key = []
        if not no_of_elevator:
            missing_req_key.append('no_of_elevator')
        if not min_floor:
            missing_req_key.append('min_floor')
        if not max_floor:
            missing_req_key.append('max_floor')
        if missing_req_key:
            response_data['message']="Missing value for {}".format(missing_req_key)
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=400) 
        if ((no_of_elevator>0) and (min_floor<max_floor)):
            elevator = Elevator.objects.all()
            if elevator:
                response_data['message']="Elevators are already set with no_of_elevator:{}, min_floor:{} , max_floor:{} ".format(elevator.values()[0]['no_of_elevator'], elevator.values()[0]['min_floor'],elevator.values()[0]['max_floor'])
            else:
                try: 
                    elevator = Elevator.objects.create(no_of_elevator=no_of_elevator, min_floor=min_floor, max_floor=max_floor) 
                    # TODO: optimize this insertion
                    for  i in range(1,no_of_elevator+1):
                        elevator_car = ElevatorCar.objects.create(elevator_no=i, current_floor=min_floor)
                    response_data['message']="updated"
                except:
                    response_data['message']="Not updated"
        else:
            response_data['message']="min_floor can't be greater than or equal to max_floor"  
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data['message']="method not allowed"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=405)

@csrf_exempt
def request_elevator(request):
    response_data={}
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        try:
            request = json.loads(body_unicode)
        except:
            response_data['message']="request body format is incorrect"
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
        elevator_no = request.get('elevator_no')
        destination_floor = request.get('destination_floor')
        missing_req_key = []
        if not elevator_no:
            missing_req_key.append('elevator_no')
        if not destination_floor:
            missing_req_key.append('destination_floor')
        if missing_req_key: 
            response_data['message']="Missing value for {}".format(missing_req_key)   
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
        elevator = Elevator.objects.all()
        if not elevator:
            response_data['message']="Elevator not initialized" 
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
        if (((elevator_no>0) and (elevator_no<=elevator.values()[0]['no_of_elevator'])) and  ((destination_floor>=elevator.values()[0]['min_floor']) and (destination_floor<=elevator.values()[0]['max_floor']))):
            elevator_car = ElevatorCar.objects.filter(elevator_no=elevator_no)
            if elevator_car.values()[0]['is_underMaintenance']:
                response_data['message']="Elevator selected is UNDER MAINTENANCE"
                return HttpResponse(json.dumps(response_data), content_type="application/json",status=202)
            else:
                elevator_request = ElevatorRequest.objects.create(elevator_no=elevator_no, destination_floor=destination_floor)
                response_data['message']="Request made successfully"
        else:
            response_data['message']="Request made is out of system"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data['message']="method not allowed"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=405)

@csrf_exempt
def fetch_request(request, elevator_no):
    response_data={}
    if request.method == 'GET':
        elevator = Elevator.objects.all()
        if ((elevator_no>0) and (elevator_no<=elevator.values()[0]['no_of_elevator'])):
            requested_floor = list(ElevatorRequest.objects.filter(elevator_no=elevator_no).distinct("destination_floor").values_list('destination_floor',flat=True))
            response_data['requested_floors']=requested_floor
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=200)
        else:
            response_data['message']="elevator_no is out of system"
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
    else:
        response_data['message']="method not allowed"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=405)

@csrf_exempt
def fetch_destination(request, elevator_no):
    response_data={}
    if request.method == 'GET':
        elevator = Elevator.objects.all()
        if ((elevator_no>0) and (elevator_no<=elevator.values()[0]['no_of_elevator'])):
            elevator_car = ElevatorCar.objects.filter(elevator_no=elevator_no)
            if elevator_car.values()[0]['is_underMaintenance']:
                response_data['message']="Elevator selected is UNDER MAINTENANCE"
                return HttpResponse(json.dumps(response_data), content_type="application/json",status=202)
            next_destination_floor = elevator_car.values()[0]['destination_floor']
            response_data['next_destination_floor']=next_destination_floor
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=200)
        else:
            response_data['message']="elevator_no is out of system"
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
    else:
        response_data['message']="method not allowed"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=405)

@csrf_exempt
def fetch_direction(request, elevator_no):
    response_data={}
    if request.method == 'GET':
        elevator = Elevator.objects.all()
        if ((elevator_no>0) and (elevator_no<=elevator.values()[0]['no_of_elevator'])):
            elevator_car = ElevatorCar.objects.filter(elevator_no=elevator_no)
            if elevator_car.values()[0]['is_underMaintenance']:
                response_data['message']="Elevator selected is UNDER MAINTENANCE"
                return HttpResponse(json.dumps(response_data), content_type="application/json",status=202)
            if elevator_car.values()[0]['moving_status'] in [0,1,-1]:
                moving_status = 'STOPPED' if elevator_car.values()[0]['moving_status']==0 else 'UP' if elevator_car.values()[0]['moving_status']==1 else 'DOWN'
                response_data['moving_status']=moving_status
                return HttpResponse(json.dumps(response_data), content_type="application/json",status=200)
            else:
                response_data['message']="Problem with moving status recorded"
                return HttpResponse(json.dumps(response_data), content_type="application/json",status=502)
        else:
            response_data['message']="elevator_no is out of system"
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
    else:
        response_data['message']="method not allowed"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=405)

@csrf_exempt
def put_under_maintenance(request, elevator_no):
    response_data={}
    if request.method == 'POST':
        pass
    else:
        response_data['message']="method not allowed"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=405)

@csrf_exempt
def operate_door(request, elevator_no):
    response_data={}
    if request.method == 'POST':
        pass
    else:
        response_data['message']="method not allowed"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=405)