from rest_framework import serializers
from .models import *

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'
        # fields = ['no_of_elevator', 'min_floor', 'max_floor']

    def validate(self, validate_data):
        no_of_elevator = validate_data.get('no_of_elevator')
        min_floor = validate_data.get('min_floor')
        max_floor = validate_data.get('max_floor')
        if ((no_of_elevator>0) and (min_floor<max_floor)):
            elevator = Elevator.objects.all()
            if elevator:
                validation_error="Elevators are already set with no_of_elevator:{}, min_floor:{} , max_floor:{} ".format(elevator.values()[0]['no_of_elevator'], elevator.values()[0]['min_floor'],elevator.values()[0]['max_floor'])
            else:
                return validate_data
        else: 
            validation_error="no_of_elevator should be greater than 0 and min_floor can't be greater than or equal to max_floor"

        raise serializers.ValidationError(validation_error)


        # return super().validate(attrs)