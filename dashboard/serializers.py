from rest_framework import serializers
from .models import *


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'workspace', 'assigned_to', 'priority', 'task_status', 'description', 'planned_start_date', 'planned_end_date', 'file']


class Self_TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Self_Task
        fields = ['id', 'title', 'workspace', 'assigned_to', 'priority', 'task_status', 'description', 'planned_start_date', 'planned_end_date', 'file']

class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = ['name', 'team', 'staff', 'slug']
        extra_kwargs = {
            'slug':{
                'read_only':True,
            },
        }

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description']


# class StaffUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StaffUser
#         fields = ['user_id', 'name', 'email', 'password', 'team']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'workspace', 'assigned_to', 'priority', 'issue_status', 'description', 'planned_start_date', 'planned_end_date', 'file']


class AttendaceInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['staff_user', 'in_time'] 


class AttendaceOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['staff_user', 'out_time'] 


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['from_date', 'to_date', 'descritpion', 'user', 'type'] 


class HolidaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holidays
        fields = ['name', 'day', 'month', 'description'] 