from dashboard.models import Holidays, Notification, StaffUser
from datetime import datetime


def holiday_notify_users():

    today = datetime.now()
    user_obj = StaffUser.objects.filter(active_status=True, is_employee=True)
    holidays = Holidays.objects.filter(status=True)
    # print('-----today date and time------', today, today.hour, today.minute)
    for holiday in holidays:
        # print('----holiday-----', holiday, holiday.month)
        if holiday.month == today.strftime('%B') and holiday.day == int(today.day)-1 and today.hour == 23 and today.minute == 30:
            # print('-----inside today create holiday notifications-----')
            for user in user_obj:
                # print('-------for every user---')
                Notification.objects.create(staff_mem=user, title="Tomorrow will be declared as holiday, on behalf of " + holiday.name, content=holiday.description)    
    