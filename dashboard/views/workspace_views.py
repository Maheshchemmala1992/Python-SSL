from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import datetime

from dashboard.models import *
from dashboard.forms import *
from dashboard.serializers import *

from django.conf import settings

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
def is_authenticated(f):
    def wrap(request, *args, **kwargs):
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


def is_staff_at_work(f):
    def wrap(request, *args, **kwargs):
        staff_in_work = []
        list_staff_ = WorkSpace.objects.filter(status=True).values('staff__name')

        for staff in list_staff_:
            staff_in_work.append(staff['staff__name'])

        if request.session['user_name'] in staff_in_work or request.session['is_admin'] == True:
            return f(request, *args, **kwargs)

        messages.info(request, 'You have no workspace yet..!')
        return redirect("home")
    wrap.__doc__ = f.__doc__
    # wrap.__name__ = f.__name__
    return wrap

def self_task_list(request,name):
    usr=User.objects.get(username=request.session['user_name']).id
    staff=StaffUser.objects.get(user_id_id=usr).id
    workspace_obj = WorkSpace.objects.filter(slug=name)
    self_task = Self_Task.objects.filter(status=True, workspace__slug=name,assigned_by_id=staff).order_by('-id')
    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    val=[]
    for t in self_task:
               
        d = t.created_on.strftime("%m/%d/%Y, %H:%M:%S")
        dt, tm = d.split(', ')
        mnt, dy, yr = dt.split('/')
        hrs,mt,sc = tm.split(':')
        dttm = ''.join([yr,mnt,dy,hrs,mt,sc])
        val.append((dttm,t))
    val=[r for r in sorted(val,key=lambda x:x[0],reverse=True)]
    return val 
  
  
def task_list(request,name):
    workspace_obj = WorkSpace.objects.filter(slug=name)
    tasks = Task.objects.filter(status=True, workspace__slug=name).order_by('-id')
    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    val=[]
    for t in tasks:
               
        d = t.created_on.strftime("%m/%d/%Y, %H:%M:%S")
        dt, tm = d.split(', ')
        mnt, dy, yr = dt.split('/')
        hrs,mt,sc = tm.split(':')
        dttm = ''.join([yr,mnt,dy,hrs,mt,sc])
        val.append((dttm,t))
    val=[r for r in sorted(val,key=lambda x:x[0],reverse=True)]
    return val 

def issue_list(request,name):
    workspace_obj = WorkSpace.objects.filter(slug=name)
    issues = Issue.objects.filter(status=True, workspace__slug=name).order_by('-id')
    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    val=[]
    for t in issues:
               
        d = t.created_on.strftime("%m/%d/%Y, %H:%M:%S")
        dt, tm = d.split(', ')
        mnt, dy, yr = dt.split('/')
        hrs,mt,sc = tm.split(':')
        dttm = ''.join([yr,mnt,dy,hrs,mt,sc])
        val.append((dttm,t))
    val=[r for r in sorted(val,key=lambda x:x[0],reverse=True)]
    return val 
@is_authenticated
@is_staff_at_work
def workspace_view(request, name):
    print('---------kkkkkkkkkkkkkkkkk---------',name,request.session['user_name'])
    if request.method == 'POST':
        usr=User.objects.get(username=request.session['user_name']).id
        staff=StaffUser.objects.get(user_id_id=usr).id
        workspace_obj = WorkSpace.objects.filter(slug=name)
        employees = StaffUser.objects.filter(active_status=True, is_employee=True)
        
        
        category = request.POST.get('category', '')
        category1 = request.POST.get('category1', '')
        category2 = request.POST.get('category2', '')
        if category=="self_task":
            date_from = request.POST.get('date_from', '')
            date_to = request.POST.get('date_to', '')
            self_task = Self_Task.objects.filter(status=True, workspace__slug=name,assigned_by_id=staff).order_by('-created_on')
            
            if date_from and date_to:
                transactions = []
                
                for e in [self_task]:
                    
                    for t in e:
                        d = t.created_on.strftime("%m/%d/%Y, %H:%M:%S")
                        dt, tm = d.split(', ')
                        mnt, dy, yr = dt.split('/')
                        hrs,mt,sc = tm.split(':')
                        dttm = ''.join([yr,mnt,dy,hrs,mt,sc])
                        transactions.append((dttm,t))
                final_transactions = [r for r in sorted(transactions,key=lambda x:x[0],reverse=False)]
                yrf,mntf, dyf = date_from.split('-')
                yrt,mntt, dyt = date_to.split('-')
                dttmf = ''.join([yrf,mntf,dyf])
                dttmt = ''.join([yrt,mntt,dyt])
                new_transactions = []
                for val in final_transactions:
                    
                    strdt = val[0]
                    st = strdt[:8]
                    if int(dttmf)<=int(st) and int(dttmt)>=int(st):
                        new_transactions.append(val)
                
                task=task_list(request,name)
                issue=issue_list(request,name)
                
            return render(request, 'dashboard/workspace.html', {'obj1':new_transactions,'tasks':task, 'issues':issue, 'employees':employees, 'workspace':workspace_obj})
        if category1=="task":
            date_from = request.POST.get('date_from1', '')
            date_to = request.POST.get('date_to1', '')
            assigned_to = request.POST.get('assigned_to', '')
            task = Task.objects.filter(status=True, workspace__slug=name,assigned_to_id=assigned_to).order_by('-created_on')
            
            if date_from and date_to:
                transactions = []
                
                for e in [task]:
                    
                    for t in e:
                        d = t.created_on.strftime("%m/%d/%Y, %H:%M:%S")
                        dt, tm = d.split(', ')
                        mnt, dy, yr = dt.split('/')
                        hrs,mt,sc = tm.split(':')
                        dttm = ''.join([yr,mnt,dy,hrs,mt,sc])
                        transactions.append((dttm,t))
                final_transactions = [r for r in sorted(transactions,key=lambda x:x[0],reverse=False)]
                yrf,mntf, dyf = date_from.split('-')
                yrt,mntt, dyt = date_to.split('-')
                dttmf = ''.join([yrf,mntf,dyf])
                dttmt = ''.join([yrt,mntt,dyt])
                new_transactions = []
                for val in final_transactions:
                    
                    strdt = val[0]
                    st = strdt[:8]
                    if int(dttmf)<=int(st) and int(dttmt)>=int(st):
                        new_transactions.append(val)
                print('---------kkkkkkkkkkkkkkkkk---------',final_transactions)
                self_task=self_task_list(request,name)
                issue=issue_list(request,name)
                
            return render(request, 'dashboard/workspace.html', {'obj1':self_task,'tasks':new_transactions, 'issues':issue, 'employees':employees, 'workspace':workspace_obj}) 
        if category2=="issue":
            date_from = request.POST.get('date_from1', '')
            date_to = request.POST.get('date_to1', '')
            assigned_to = request.POST.get('assigned_to', '')
            issues = Issue.objects.filter(status=True, workspace__slug=name,assigned_to_id=assigned_to).order_by('-created_on')
            
            if date_from and date_to:
                transactions = []
                
                for e in [issues]:
                    
                    for t in e:
                        d = t.created_on.strftime("%m/%d/%Y, %H:%M:%S")
                        dt, tm = d.split(', ')
                        mnt, dy, yr = dt.split('/')
                        hrs,mt,sc = tm.split(':')
                        dttm = ''.join([yr,mnt,dy,hrs,mt,sc])
                        transactions.append((dttm,t))
                final_transactions = [r for r in sorted(transactions,key=lambda x:x[0],reverse=False)]
                yrf,mntf, dyf = date_from.split('-')
                yrt,mntt, dyt = date_to.split('-')
                dttmf = ''.join([yrf,mntf,dyf])
                dttmt = ''.join([yrt,mntt,dyt])
                new_transactions = []
                for val in final_transactions:
                    
                    strdt = val[0]
                    st = strdt[:8]
                    if int(dttmf)<=int(st) and int(dttmt)>=int(st):
                        new_transactions.append(val)
                print('---------kkkkkkkkkkkkkkkkk---------',final_transactions)
                self_task=self_task_list(request,name)
                task=task_list(request,name)
                
            return render(request, 'dashboard/workspace.html', {'obj1':self_task,'tasks':task, 'issues':new_transactions, 'employees':employees, 'workspace':workspace_obj})
        
    else:    
        usr=User.objects.get(username=request.session['user_name']).id
        staff=StaffUser.objects.get(user_id_id=usr).id
        workspace_obj = WorkSpace.objects.filter(slug=name)
        tasks = Task.objects.filter(status=True, workspace__slug=name).order_by('-id')
        issues = Issue.objects.filter(status=True, workspace__slug=name).order_by('-id')
        self_task = Self_Task.objects.filter(status=True, workspace__slug=name,assigned_by_id=staff).order_by('-id')
        
        employees = StaffUser.objects.filter(active_status=True, is_employee=True)
        
        val=[]
        val1=[]
        val2=[]
        for t in self_task:
               
            d = t.created_on.strftime("%m/%d/%Y, %H:%M:%S")
            dt, tm = d.split(', ')
            mnt, dy, yr = dt.split('/')
            hrs,mt,sc = tm.split(':')
            dttm = ''.join([yr,mnt,dy,hrs,mt,sc])
            val.append((dttm,t))
        val=[r for r in sorted(val,key=lambda x:x[0],reverse=True)]
        for t in tasks:
               
            d = t.created_on.strftime("%m/%d/%Y, %H:%M:%S")
            dt, tm = d.split(', ')
            mnt, dy, yr = dt.split('/')
            hrs,mt,sc = tm.split(':')
            dttm = ''.join([yr,mnt,dy,hrs,mt,sc])
            val1.append((dttm,t))
        val1=[r for r in sorted(val1,key=lambda x:x[0],reverse=True)]
        for t in issues:
               
            d = t.created_on.strftime("%m/%d/%Y, %H:%M:%S")
            dt, tm = d.split(', ')
            mnt, dy, yr = dt.split('/')
            hrs,mt,sc = tm.split(':')
            dttm = ''.join([yr,mnt,dy,hrs,mt,sc])
            val2.append((dttm,t))
        val2=[r for r in sorted(val2,key=lambda x:x[0],reverse=True)]
        return render(request, 'dashboard/workspace.html', {'tasks':val1, 'issues':val2, 'employees':employees, 'workspace':workspace_obj,'obj1':val,'name':name
        })
    

@is_authenticated
@is_staff_at_work
def document_list(request):
   
    
    if request.method == 'POST':
        print('---------kkkkkkkkkkkkkkkkk---------')
        id = request.POST.get('edit_id')
        task_obj = Task.objects.get(status=True, id=id)
        file_name=request.FILES.get('file1')
        task_obj.update_file = file_name
        task_obj.save()
    else:
        id=request.GET.get('edit_id')
        task_obj = Task.objects.get(status=True, id=id).workspace_id 
        list_val=Task.objects.filter(workspace_id=task_obj).file
        for i in list_val:
            print('----------------------',i)

@is_authenticated
@is_staff_at_work

def task_detail_update_view(request, id, workspace_slug):
    print('---------task_obj-----------')
    task_obj = Task.objects.get(status=True, id=id, workspace__slug=workspace_slug)
    prev_assigned_user = task_obj.assigned_to.name

    if request.method == 'POST':
        # planned_start_date = request.POST.get('planned_start_date')
        actual_start_date = request.POST.get('actual_start_date')
        # planned_end_date = request.POST.get('planned_end_date')
        actual_end_date = request.POST.get('actual_end_date')
        description = request.POST.get('description')
        assigned_to = request.POST.get('assigned_to')
        priority = request.POST.get('priority')
        file_name=request.FILES.get('file')
        staff_mem = StaffUser.objects.get(id=assigned_to)
        # if planned_start_date != '':
        #     task_obj.planned_start_date = datetime.strptime(planned_start_date, "%Y-%m-%dT%H:%M")
        # if planned_end_date != '':
        #     task_obj.planned_end_date = datetime.strptime(planned_end_date, "%Y-%m-%dT%H:%M")
        if actual_start_date != '':
            task_obj.actual_start_date = datetime.strptime(actual_start_date, "%Y-%m-%dT%H:%M")
        if actual_end_date != '':
            task_obj.actual_end_date = datetime.strptime(actual_end_date, "%Y-%m-%dT%H:%M")

        task_obj.priority = priority
        task_obj.description = description
        task_obj.assigned_to = staff_mem
        task_obj.file = file_name
        task_obj.save()
        print('--------------------',task_obj.assigned_to.name)
        
        Notification.objects.create(staff_mem_id=task_obj.assigned_to.id, title='There is an update with the task', content=str(task_obj.title) + ' task has been updated...')

        if prev_assigned_user != staff_mem.name:
            from_mail = settings.EMAIL_HOST_USER
            to_mail = staff_mem.email
            subject = 'A new task has been added for you..'

            message = render_to_string('{0}/templates/mail_templates/task_assigned.html'.format(settings.BASE_DIR),{'name':staff_mem.name, 'workspace':task_obj.workspace.name, 'team':task_obj.workspace.team.name, 'task':task_obj.title, 'status':task_obj.get_task_status_display(), 'priority':task_obj.get_priority_display(), 'end_date':task_obj.planned_end_date})
            
            msg = EmailMultiAlternatives(subject, message, from_mail, [to_mail])
            msg.attach_alternative(message, 'text/html')
            msg.send(fail_silently=False)

        messages.success(request, 'Task update success...')
        return redirect('/' + task_obj.workspace.slug + '/' + str(task_obj.id)+'/task')
        
    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    task_comments = TaskComment.objects.filter(status=True, task=task_obj).order_by('-id')
    return render(request, 'dashboard/task_detail_update.html', {'object':task_obj, 'employees':employees, 'comments':task_comments, 'id':id})


@is_authenticated
@is_staff_at_work
def self_task_detail_update_view(request, id, workspace_slug):
    print('---------task_obj-----------')
    task_obj = Self_Task.objects.get(status=True, id=id, workspace__slug=workspace_slug)
    prev_assigned_user = task_obj.assigned_by.name
    if request.method == 'POST':
        # planned_start_date = request.POST.get('planned_start_date')
        actual_start_date = request.POST.get('actual_start_date')
        # planned_end_date = request.POST.get('planned_end_date')
        actual_end_date = request.POST.get('actual_end_date')
        description = request.POST.get('description')
        assigned_to = request.POST.get('assigned_to')
        priority = request.POST.get('priority')
        file_name=request.FILES.get('file')
        staff_mem = StaffUser.objects.get(id=assigned_to)
        # if planned_start_date != '':
        #     task_obj.planned_start_date = datetime.strptime(planned_start_date, "%Y-%m-%dT%H:%M")
        # if planned_end_date != '':
        #     task_obj.planned_end_date = datetime.strptime(planned_end_date, "%Y-%m-%dT%H:%M")
        if actual_start_date != '':
            task_obj.actual_start_date = datetime.strptime(actual_start_date, "%Y-%m-%dT%H:%M")
        if actual_end_date != '':
            task_obj.actual_end_date = datetime.strptime(actual_end_date, "%Y-%m-%dT%H:%M")

        task_obj.priority = priority
        task_obj.description = description
        task_obj.assigned_to = staff_mem
        task_obj.file = file_name
        task_obj.save()
        
        
        Notification.objects.create(staff_mem_id=task_obj.assigned_to.id, title='There is an update with the task', content=str(task_obj.title) + ' task has been updated...')

        if prev_assigned_user == staff_mem.name:
            from_mail = settings.EMAIL_HOST_USER
            to_mail = staff_mem.email
            subject = 'A new task has been added for you..'

            message = render_to_string('{0}/templates/mail_templates/task_assigned.html'.format(settings.BASE_DIR),{'name':staff_mem.name, 'workspace':task_obj.workspace.name, 'team':task_obj.workspace.team.name, 'task':task_obj.title, 'status':task_obj.get_task_status_display(), 'priority':task_obj.get_priority_display(), 'end_date':task_obj.planned_end_date})
            
            msg = EmailMultiAlternatives(subject, message, from_mail, [to_mail])
            msg.attach_alternative(message, 'text/html')
            # msg.send(fail_silently=False)

        messages.success(request, 'Task update success...')
        return redirect('/' + task_obj.workspace.slug + '/' + str(task_obj.id)+'/self-task')
        
    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    task_comments = Self_TaskComment.objects.filter(status=True, task=task_obj).order_by('-id')
    return render(request, 'dashboard/self_task_detail_update.html', {'object':task_obj, 'employees':employees, 'comments':task_comments, 'id':id})

@is_authenticated
@is_staff_at_work
def self_task_email(request, id, workspace_slug):
    task_obj = Self_Task.objects.get(status=True, id=id, workspace__slug=workspace_slug)
    prev_assigned_user = task_obj.assigned_by.name
    if request.method == 'POST':
        email = request.POST.get('email')
        print('--------------------',task_obj.assigned_by.name,email)
        from_mail = settings.EMAIL_HOST_USER
        to_mail = email
        subject = 'A new task has been added for you..'

        message = render_to_string('{0}/templates/mail_templates/task_assigned.html'.format(settings.BASE_DIR),{'name':task_obj.assigned_by.name, 'workspace':task_obj.workspace.name, 'team':task_obj.workspace.team.name, 'task':task_obj.title, 'status':task_obj.get_task_status_display(), 'priority':task_obj.get_priority_display(), 'end_date':task_obj.planned_end_date})
        
        msg = EmailMultiAlternatives(subject, message, from_mail, [to_mail])
        msg.attach_alternative(message, 'text/html')
        # msg.attach_file(str(task_obj.file))
        # msg.send(fail_silently=False)
        return redirect('/' + task_obj.workspace.slug)
@is_authenticated
@is_staff_at_work
def issue_detail_update_view(request, id, workspace_slug):

    issue_obj = Issue.objects.get(status=True, id=id, workspace__slug=workspace_slug)
    prev_assigned_user = issue_obj.assigned_to.name

    if request.method == 'POST':
        priority = request.POST.get('priority')
        assigned_to = request.POST.get('assigned_to')
        description = request.POST.get('description')
        actual_end_date = request.POST.get('actual_end_date')
        # planned_end_date = request.POST.get('planned_end_date')
        actual_start_date = request.POST.get('actual_start_date')
        # planned_start_date = request.POST.get('planned_start_date')
        staff_mem = StaffUser.objects.get(id=assigned_to)
        
        # if planned_start_date != '':
        #     issue_obj.planned_start_date = datetime.strptime(planned_start_date, "%Y-%m-%dT%H:%M")
        # if planned_end_date != '':
        #     issue_obj.planned_end_date = datetime.strptime(planned_end_date, "%Y-%m-%dT%H:%M")
        if actual_start_date != '':
            issue_obj.actual_start_date = datetime.strptime(actual_start_date, "%Y-%m-%dT%H:%M")
        if actual_end_date != '':
            issue_obj.actual_end_date = datetime.strptime(actual_end_date, "%Y-%m-%dT%H:%M")

        issue_obj.priority = priority
        issue_obj.description = description
        issue_obj.assigned_to = staff_mem
        issue_obj.save()

        Notification.objects.create(staff_mem=issue_obj.assigned_to, title='There is an update with the task', content=issue_obj.title + ' issue has been updated...')

        if prev_assigned_user != staff_mem.name:
            from_mail = settings.EMAIL_HOST_USER
            to_mail = staff_mem.email
            subject = 'A new task has been added for you..'
            message = render_to_string('{0}/templates/mail_templates/issue_assigned.html'.format(settings.BASE_DIR),{'name':staff_mem.name, 'workspace':issue_obj.workspace.name, 'team':issue_obj.workspace.team.name, 'task':issue_obj.title, 'status':issue_obj.get_issue_status_display(), 'priority':issue_obj.get_priority_display(), 'end_date':issue_obj.planned_end_date})
            
            msg = EmailMultiAlternatives(subject, message, from_mail, [to_mail])
            msg.attach_alternative(message, 'text/html')
            msg.send(fail_silently=False)

        messages.success(request, 'Issue update success...')
        return redirect('/' + issue_obj.workspace.slug + '/' + str(issue_obj.id) + '/issue')

    employees = StaffUser.objects.filter(active_status=True, is_employee=True)
    issue_comments = IssueComment.objects.filter(status=True, issue=issue_obj).order_by('-id')
    return render(request, 'dashboard/issue_detail_update.html', {'object':issue_obj, 'employees':employees, 'comments':issue_comments, 'id':id})


@is_authenticated
def task_delete(request, id):

    task_obj = Task.objects.get(status=True, id=id)
    Notification.objects.create(staff_mem=task_obj.assigned_to, title='task has been removed from workspace', content=task_obj.title + ' has been removed from ' + task_obj.workspace.name)
    task_obj.delete()
    messages.success(request, task_obj.task_id + ' delete success...')
    return redirect('/'+task_obj.workspace.slug)


@is_authenticated
def self_task_delete(request, id):

    task_obj = Self_Task.objects.get(status=True, id=id)
    Notification.objects.create(staff_mem=task_obj.assigned_by, title='task has been removed from workspace', content=task_obj.title + ' has been removed from ' + task_obj.workspace.name)
    task_obj.delete()
    messages.success(request, task_obj.task_id + ' delete success...')
    return redirect('/'+task_obj.workspace.slug)

@is_authenticated
def issue_delete(request, id):

    issue_obj = Issue.objects.get(id=id, status=True)
    Notification.objects.create(staff_mem=issue_obj.assigned_to, title='Issue has been removed from workspace', content=issue_obj.title + ' has been removed from ' + issue_obj.workspace.name)
    messages.success(request, issue_obj.issue_id + ' delete success...')
    issue_obj.delete()
    return redirect('/'+issue_obj.workspace.slug)