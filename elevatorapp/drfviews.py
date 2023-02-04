from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .serializer import ElevatorSerializer
from .models import *

class ElevatorViewSet(mixins.CreateModelMixin, 
                      viewsets.GenericViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer