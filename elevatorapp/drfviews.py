from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from django.shortcuts import get_object_or_404
from .serializer import ElevatorSerializer, ElevatorRequestSerializer, ElevatorCarSerializer
from .models import *
from .background import elevator_task, door_task
from background_task.models import Task

class ElevatorViewSet(mixins.CreateModelMixin, 
                      viewsets.GenericViewSet):

    def create(self, request, *args, **kwargs):
        no_of_elevator = request.data.get('no_of_elevator')
        min_floor = request.data.get('min_floor')
        max_floor = request.data.get('max_floor')
        serializer = ElevatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(no_of_elevator=no_of_elevator, min_floor=min_floor, max_floor=max_floor) 
        for  i in range(1,no_of_elevator+1):
            elevator_car = ElevatorCar.objects.create(elevator_no=i, current_floor=min_floor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ElevatorRequestViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        elevator_no = request.data.get('elevator_no')
        destination_floor = request.data.get('destination_floor')
        serializer = ElevatorRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(elevator_no=elevator_no, destination_floor=destination_floor) 
        tasks = Task.objects.filter(verbose_name="elevator_task_elevator{}".format(elevator_no))
        if len(tasks) == 0:
            elevator_task(elevator_no, verbose_name="elevator_task_elevator{}".format(elevator_no))
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def retrieve(self, request, pk=None, *args, **kwargs):
        requested_floor = list(ElevatorRequest.objects.filter(elevator_no=pk).distinct("destination_floor").values_list('destination_floor',flat=True))
        return Response({"requested_floors": requested_floor})

class ElevatorCarViewSet(viewsets.GenericViewSet):
    queryset = ElevatorCar.objects.all()
    serializer_class = ElevatorCarSerializer
    @action(detail=False, methods=['post'], url_path='put/under-maintenance', url_name="under_maintenance")
    def under_maintenance(self, request):
        serializer = ElevatorCarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        elevator_no = request.data.get('elevator_no')
        elevator_car = ElevatorCar.objects.filter(elevator_no=elevator_no)
        if elevator_car:
            ElevatorCar.objects.filter(elevator_no=elevator_no).update(is_underMaintenance=True)
            ElevatorCar.objects.filter(elevator_no=elevator_no).update(is_doorOpen=True)
            return Response({'message': 'Elevator {} Marked UNDER MAINTENANCE'.format(elevator_no)})
        else:
            return Response({"message": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='operate-door', url_name="operate_door")
    def operate_door(self, request):
        serializer = ElevatorCarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        elevator_no = request.data.get('elevator_no')
        elevator_car = ElevatorCar.objects.filter(elevator_no=elevator_no)
        if elevator_car and request.data.get('is_doorOpen'):
            tasks = Task.objects.filter(verbose_name="door_task_elevator{}".format(elevator_no))
            if len(tasks) == 0:
                door_task(elevator_no, verbose_name="door_task_elevator{}".format(elevator_no))
                return Response({"message": "Door OPENED"})
            else:
                return Response({"message": "Door is already in OPEN state"})
        else:
            return Response({"message": "Invalid request body"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='fetch-destination', url_name="fetch_destination")
    def fetch_destination(self, request, pk=None):
        elevator_no = pk
        serializer = ElevatorCarSerializer(data = {"elevator_no":elevator_no})
        serializer.is_valid(raise_exception=True)
        elevator_car = ElevatorCar.objects.filter(elevator_no=elevator_no)
        next_destination_floor = elevator_car.values()[0]['destination_floor']
        return Response({"next_destination_floor": next_destination_floor})
    
    @action(detail=True, methods=['get'], url_path='fetch-direction', url_name="fetch_direction")
    def fetch_direction(self, request, pk=None):
        elevator_no = pk
        serializer = ElevatorCarSerializer(data = {"elevator_no":elevator_no})
        serializer.is_valid(raise_exception=True)
        elevator_car = ElevatorCar.objects.filter(elevator_no=elevator_no)
        if elevator_car.values()[0]['moving_status'] in [0,1,-1]:
            moving_status = 'STOPPED' if elevator_car.values()[0]['moving_status']==0 else 'UP' if elevator_car.values()[0]['moving_status']==1 else 'DOWN'
            return Response({"moving_status": moving_status})
        else:
            return Response({"Problem with moving status recorded"},status=status.HTTP_400_BAD_REQUEST)

