from rest_framework import serializers, status
from .models import *
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text

class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        else: self.detail = {'detail': force_text(self.default_detail)}

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        # fields = '__all__'
        fields = ['no_of_elevator', 'min_floor', 'max_floor']

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

class ElevatorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequest
        # fields = '__all__'
        fields = ['elevator_no','destination_floor']

    def validate(self, validate_data):
        elevator_no = validate_data.get('elevator_no')
        destination_floor = validate_data.get('destination_floor')
        elevator = Elevator.objects.all()
        if not elevator:
            validation_error = "Elevator not initialized"
        if (((elevator_no>0) and (elevator_no<=elevator.values()[0]['no_of_elevator'])) and  ((destination_floor>=elevator.values()[0]['min_floor']) and (destination_floor<=elevator.values()[0]['max_floor']))):
            elevator_car = ElevatorCar.objects.filter(elevator_no=elevator_no)
            if elevator_car.values()[0]['is_underMaintenance']:
                raise CustomValidation("Elevator selected is UNDER MAINTENANCE", "ElevatorCar", status_code=status.HTTP_202_CONFLICT)
            else:
                return validate_data
        else:
            validation_error = "Request made is out of system"
        raise serializers.ValidationError(validation_error)