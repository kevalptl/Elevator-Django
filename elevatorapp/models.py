from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import locale
from django.core.exceptions import ValidationError

class Elevator(models.Model):
    no_of_elevator = models.IntegerField(null=False, blank=False)
    min_floor = models.IntegerField(null=False, blank=False)
    max_floor = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return '%d %d %d' % (self.no_of_elevator,self.min_floor, self.max_floor)

class ElevatorCar(models.Model):
    Up = 1
    Down = -1
    Stopped = 0
    MOVING_STATUS_CHOICES = (
        (Up, 'Up'),
        (Down, 'Down'),
        (Stopped, 'Stopped'),
    )
    elevator_no = models.IntegerField(null=False, blank=False)
    current_floor = models.IntegerField(null=False, blank=False)
    destination_floor = models.IntegerField(null=True, blank=True)
    moving_status = models.IntegerField(choices=MOVING_STATUS_CHOICES, default=Stopped)
    is_doorOpen = models.BooleanField(default=False)
    is_underMaintenance = models.BooleanField(default=False)

class ElevatorRequest(models.Model):
    elevator_no = models.IntegerField(null=False, blank=False)
    destination_floor = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%d %d' % (self.elevator_no,self.destination_floor)
