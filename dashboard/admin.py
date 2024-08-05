from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import date_hierarchy
from django.utils.translation import check_for_language
from .models import *


class StaffUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_admin', 'is_employee', 'created_on')
    list_filter = ('active_status',)
    date_hierarchy = 'created_on'


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'issue_status', 'workspace')
    list_filter = ('issue_status', 'issue_type')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'task_status', 'workspace')
    list_filter = ('task_status',)


class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'get_staff')
    date_hierarchy = 'created_on'
    
    def get_staff(self, obj):
        return obj.staff.values('name')


class AttendaceAdmin(admin.ModelAdmin):
    list_display = ('staff_user', 'in_time', 'out_time')
    list_filter = ('staff_user__name', )
    search_fields = ('staff_user__name',)
    date_hierarchy = 'in_time'
    list_per_page = 10
    

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_date', 'to_date', 'number_of_days', 'leave_status')
    list_filter = ('leave_status', 'user__name')
    date_hierarchy = 'from_date'


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    search_fields = ('title',)


admin.site.register(Attendance, AttendaceAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(StaffUser, StaffUserAdmin)
admin.site.register(Team)
admin.site.register(WorkSpace, WorkspaceAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(TaskComment)
admin.site.register(Holidays)
admin.site.register(Notification, NotificationAdmin)