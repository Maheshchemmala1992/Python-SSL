from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg, Count, Min, Sum

from dashboard.models import *
from dashboard.forms import *
from dashboard.serializers import *
from django.conf import settings
import datetime

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def is_authenticated(f):
    def wrap(request, *args, **kwargs):
        # this check the session if userid key exist, if not it will redirect to login page
        try:
            user_obj = StaffUser.objects.get(id=request.session['id'])
        except:
            user_obj = False
        if 'id' in request.session.keys() and user_obj:
            return f(request, *args, **kwargs)

        request.session.clear()
        return redirect("login")
    wrap.__doc__ = f.__doc__
    # wrap.__name__ = f.__name__
    return wrap


@is_authenticated
def home(request):

    try:
        main_user_obj = ''
        staff_obj = ''
        workspace_obj = ''
        today = datetime.date.today()

        user_obj = StaffUser.objects.get(id=request.session.get('id'))
        employees = StaffUser.objects.filter(active_status=True, is_employee=True)
        
        full_days_in_current_month = Attendance.objects.filter(in_time__month=today.month, in_time__year=today.year, out_time__month=today.month, out_time__year=today.year, day_type='Full-day').filter(staff_user=user_obj, status=True)

        half_days_in_current_month = Attendance.objects.filter(in_time__month=today.month, in_time__year=today.year, out_time__month=today.month, out_time__year=today.year, day_type='Half-a-day').filter(staff_user=user_obj, status=True)
        leaves_taken = Leave.objects.filter(user=user_obj, leave_status='Approved', from_date__year=today.year, status=True).aggregate(total_days=Sum('number_of_days'))['total_days']

        if leaves_taken == None:
            bal_leaves = int(user_obj.leaves_provided)
        else:
            bal_leaves = int(user_obj.leaves_provided) - int(leaves_taken)

        if request.session.get('is_admin') == False:
            workspace = WorkSpace.objects.filter(status=True, staff=user_obj)
            aproved_leaves = Leave.objects.filter(user=user_obj, leave_status='Approved', status=True).count()
            pending_leaves = Leave.objects.filter(user=user_obj, leave_status='Pending', status=True).count()
            rejected_leaves = Leave.objects.filter(user=user_obj, leave_status='Rejected', status=True).count()
        else:
            aproved_leaves = Leave.objects.filter(leave_status='Approved', status=True).count()
            pending_leaves = Leave.objects.filter(leave_status='Pending', status=True).count()
            rejected_leaves = Leave.objects.filter(leave_status='Rejected', status=True).count()
            workspace = WorkSpace.objects.filter(status=True)

        if request.method == 'POST':
            invite_email = request.POST.get('email')
            workspace_id = request.POST.get('workspace')
            workspace_obj = WorkSpace.objects.get(id=workspace_id)

            try:
                main_user_obj = User.objects.get(email=invite_email)
                staff_obj = StaffUser.objects.get(email=invite_email)
            except Exception as e:
                # print('----exception error in invite----', e)
                name = invite_email.split('@')[0]
                main_user_obj = User.objects.create_user(username=name, email=invite_email, password=str(name)+str(123))
                staff_obj = StaffUser.objects.create(name=name, email=invite_email, password=str(name)+str(123))

                from_mail = settings.EMAIL_HOST_USER
                to_email = main_user_obj.email
                body = "DITS staff acccount has been created: \n\n"\
                        "User Name : {} ".format(staff_obj.name)+'\n'+\
                        "Email: {} ".format(staff_obj.email)+'\n'+\
                        "Password: {} ".format(staff_obj.password)+'\n'+\
                        "link: {} ".format(settings.BASE_DOMAIN + '/login')

                send_mail(
                    'Welcome to DITS Task Management App',
                    body,
                    from_mail,
                    [to_email],
                    fail_silently=False,
                )
            if not staff_obj in workspace_obj.staff.all():
                workspace_obj.staff.add(staff_obj)
                workspace_obj.save()
                Notification.objects.create(staff_mem=staff_obj, title='you were added to a new workspace', content=workspace_obj.name + ' you were added to this workspace.')
            else:
                messages.error(request, 'Member already exist in provided workspace.')

            from_mail = settings.EMAIL_HOST_USER
            subject = "You've been invited to the new Workspace..."
            message = render_to_string('{0}/templates/mail_templates/join_team_invitation.html'.format(settings.BASE_DIR),{'url':settings.BASE_DOMAIN + '/' + workspace_obj.slug})
            msg = EmailMultiAlternatives(subject, message, from_mail, [invite_email])
            msg.attach_alternative(message, 'text/html')
            msg.send(fail_silently=False)

        if request.GET.get('id'):
            if request.method == "GET" and request.is_ajax():
                task_obj = Task.objects.get(id=request.GET.get('id'))
                task_obj.priority = request.GET.get('priority')
                task_obj.save()

                Notification.objects.create(staff_mem=task_obj.assigned_to, title='change in priority of a task', content=task_obj.name +' priority has been changed to - ' + task_obj.priority)
                messages.success(request, 'Task priority changed successfully...')

        elif request.GET.get('iss_id'):
            if request.method == 'GET' and request.is_ajax():
                issue_obj = Issue.objects.get(id=request.GET.get('iss_id'))
                issue_obj.priority = request.GET.get('issu_priority')
                issue_obj.save()

                Notification.objects.create(staff_mem=issue_obj.assigned_to, title='change in priority of a task', content=issue_obj.name + ' priority has been changed to - ' + issue_obj.priority)
                messages.success(request, 'Issue prority changed successfully...')

    except Exception as e:
        print('-----e----', e)
        user_obj = ''
        employees = ''
        workspace = ''
        days_in_current_month = ''
        bal_leaves = ''
        aproved_leaves = ''
        pending_leaves = ''
        rejected_leaves = ''

    page = request.GET.get('page', 1)
    paginator = Paginator(workspace, 6)
    try:
        workspace = paginator.page(page)
    except PageNotAnInteger:
        workspace = paginator.page(1)
    except EmptyPage:
        workspace = paginator.page(paginator.num_pages)         
    data = {
        'obj': user_obj, 'employees':employees, 
        'workspace': workspace, 
        'len_work':len(workspace), 
        'full_days_in_current_month':len(full_days_in_current_month),
        'half_days_in_current_month':len(half_days_in_current_month),
        'bal_leaves':bal_leaves, 
        'aproved_leaves':aproved_leaves, 
        'pending_leaves':pending_leaves, 
        'rejected_leaves':rejected_leaves, 
    }
    return render(request,'dashboard/home.html', data)


@is_authenticated
def workspace_edit(request, id):
    
    workspace_obj = WorkSpace.objects.get(id=id)
    if request.method == 'POST':
        form = WorkspaceUpdateForm(request.POST, instance=workspace_obj)
        if form.is_valid():
            form.save()
            for user in workspace_obj.staff.all():
                Notification.objects.create(staff_mem=user, title=str(workspace_obj.name)+' workspace has new update', content='Workspace is updated with the new data ' + str(workspace_obj.name) + str(workspace_obj.slug) + str(workspace_obj.team.name) + str(workspace_obj.staff.all()))
            return redirect('/')
    else:
        form = WorkspaceUpdateForm(instance=workspace_obj)
    return render(request, 'dashboard/workspace_update.html', {'object':workspace_obj})


@is_authenticated
def notification_detailed_view(request, id):

    if Notification.objects.filter(id=id, status=False).exists():
        messages.info(request, 'Notification not found..')
        pass

    notified_obj = Notification.objects.get(id=id, status=True)
    notified_obj.open_status = True
    notified_obj.save()
    return render(request, 'dashboard/view_notification.html', {'obj':notified_obj})


@is_authenticated
def user_notofications_view(request):

    return render(request, 'dashboard/user_notifications.html')
