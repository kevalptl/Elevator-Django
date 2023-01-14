from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
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
        if ((no_of_elevator>0) and  (min_floor>=0)) and (max_floor>0) and (min_floor<max_floor):
            elevator = Elevator.objects.all()
            if elevator:
                response_data['message']="Elevators are already set with no_of_elevator:{}, min_floor:{} , max_floor:{} ".format(elevator.values()[0]['no_of_elevator'], elevator.values()[0]['min_floor'],elevator.values()[0]['max_floor'])
            else:
                elevator = Elevator.objects.create(no_of_elevator=no_of_elevator, min_floor=min_floor, max_floor=max_floor)
                response_data['message']="updated"
        else:
            missing_req_key = []
            if min_floor>=max_floor:
                response_data['message']="min_floor can't be greater than or equal to max_floor"
            else:
                if not no_of_elevator:
                    missing_req_key.append('no_of_elevator')
                if not min_floor:
                    missing_req_key.append('min_floor')
                if not max_floor:
                    missing_req_key.append('max_floor')
                response_data['message']="Missing value for {}".format(missing_req_key)   
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data['message']="method not allowed"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=405)
