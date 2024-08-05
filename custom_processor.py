from datetime import datetime
from dashboard.models import Holidays, Notification, StaffUser, Team, WorkSpace


def get_members(request):

    try:
        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        members = StaffUser.objects.filter(active_status=True, is_employee=True, is_admin=False).order_by('name')
        all_staff = StaffUser.objects.filter(active_status=True, is_employee=True).order_by('name')
        teams = Team.objects.filter(status=True).order_by('name')
        workspaces = WorkSpace.objects.all().order_by('name')
        notifications = Notification.objects.filter(staff_mem=user_obj, open_status=False)
        notification_obj = Notification.objects.filter(staff_mem=user_obj)
    except:
        members = ''
        teams = ''
        user_obj= ''
        workspaces = ''
        all_staff = ''
        notifications = ''
    return {'obj': user_obj, 'members':members, 'teams':teams, 'all_staff':all_staff, 'workspaces':workspaces, 'notifications':notifications, 'notifi_count':len(notifications), 'obj':notification_obj}