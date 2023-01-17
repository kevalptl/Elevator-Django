from . import views
from django.urls import path, include

app_name = 'elevatorapp'

urlpatterns = [
    path('init/elevator', views.init_elevator, name="initiate_elevator"),
    path('request/elevator', views.request_elevator, name="request_elevator"),
    path('fetch-request/<int:elevator_no>', views.fetch_request, name="fetch_request"),
    path('fetch-destination/<int:elevator_no>', views.fetch_destination, name="fetch_destination"),
    path('fetch-direction/<int:elevator_no>', views.fetch_direction, name="fetch_direction"),
    path('request/under-maintenance', views.put_under_maintenance, name="put_under_maintenance"),
    path('operate-door', views.operate_door, name="operate_door"),
    
]