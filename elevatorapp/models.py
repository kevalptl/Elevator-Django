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
