from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from django.shortcuts import get_object_or_404
from .serializer import ElevatorSerializer, ElevatorRequestSerializer
from .models import *

class ElevatorViewSet(mixins.CreateModelMixin, 
                      viewsets.GenericViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

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
    queryset = ElevatorRequest.objects.all()
    serializer_class = ElevatorRequestSerializer
    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = ElevatorRequest.objects.filter(elevator_no=pk)
        serializer = ElevatorRequestSerializer(queryset, many=True)
        return Response(serializer.data)