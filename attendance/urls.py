from django.urls import path ,include
from attendance.views import *

urlpatterns = [
    path('',home,name='attendance_home')
]
