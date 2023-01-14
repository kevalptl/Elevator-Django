from . import views
from django.urls import path, include

app_name = 'elevatorapp'

urlpatterns = [
    path('init/elevator', views.init_elevator, name="initiate_elevator"),
    
]