from django.contrib import messages
from django.http.response import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect

from dashboard.models import *


def tasK_status_change(request):

    if request.method == "GET" and request.is_ajax():
        task_obj = Task.objects.get(id=request.GET.get('id'),)
        prev_status = task_obj.get_task_status_display()
        task_obj.task_status = request.GET.get('task_status',)
        aftr_status = task_obj.get_task_status_display()
        task_obj.save()

        Notification.objects.create(staff_mem=task_obj, title='task status had been updated', content=task_obj.name + ' task status has been updated to ' + aftr_status)

        id = request.GET.get('id')
        from_mail = settings.EMAIL_HOST_USER
        to_email = task_obj.assigned_to.email
        subject = "Task Status Changed - " + task_obj.assigned_to.name
        body = "Status change for assigned task - " + task_obj.title + " : \n\n"\
                "User Name : {} ".format(task_obj.assigned_to.name)+'\n'+\
                "Workspace: {} ".format(task_obj.workspace.name)+'\n'+\
                "Task Name: {} ".format(task_obj.title)+'\n'+\
                "Previous Status: {} ".format(prev_status)+'\n'+\
                "Present Status: {} ".format(aftr_status)+'\n'+\
                "link: {}/{}/{}/task ".format(settings.CURRENT_DOMAIN, task_obj.workspace.slug, id)
        send_mail(
            subject,
            body,
            from_mail,
            [to_email],
            fail_silently=False,
        )
        
        messages.success(request, 'Task-status change success...')
    return HttpResponse('success')


def self_tasK_status_change(request):
    if request.method == "GET" and request.is_ajax():
        task_obj = Self_Task.objects.get(id=request.GET.get('id'),)
        prev_status = task_obj.get_task_status_display()
        task_obj.task_status = request.GET.get('task_status',)
        aftr_status = task_obj.get_task_status_display()
        task_obj.save()

        Notification.objects.create(staff_mem=task_obj, title='task status had been updated', content=task_obj.name + ' task status has been updated to ' + aftr_status)

        id = request.GET.get('id')
        from_mail = settings.EMAIL_HOST_USER
        to_email = task_obj.assigned_by.email
        subject = "Task Status Changed - " + task_obj.assigned_to.name
        body = "Status change for assigned task - " + task_obj.title + " : \n\n"\
                "User Name : {} ".format(task_obj.assigned_to.name)+'\n'+\
                "Workspace: {} ".format(task_obj.workspace.name)+'\n'+\
                "Task Name: {} ".format(task_obj.title)+'\n'+\
                "Previous Status: {} ".format(prev_status)+'\n'+\
                "Present Status: {} ".format(aftr_status)+'\n'+\
                "link: {}/{}/{}/task ".format(settings.CURRENT_DOMAIN, task_obj.workspace.slug, id)
        send_mail(
            subject,
            body,
            from_mail,
            [to_email],
            fail_silently=False,
        )
        
        messages.success(request, 'Task-status change success...')
    return HttpResponse('success')

def issue_status_change(request):

    if request.method == "GET" and request.is_ajax():
        issue_obj = Issue.objects.get(id=request.GET.get('id'),)
        prev_status = issue_obj.get_issue_status_display()
        issue_obj.issue_status = request.GET.get('issue_status',)
        aftr_status = issue_obj.get_issue_status_display()
        issue_obj.save()

        Notification.objects.create(staff_mem=issue_obj, title='task status had been updated', content=issue_obj.name + ' task status has been updated to ' + aftr_status)

        from_mail = settings.EMAIL_HOST_USER
        to_email = issue_obj.assigned_to.email
        subject = "Issue Status Changed - " + issue_obj.assigned_to.name
        body = "Status change for Issue raised - " + issue_obj.title + " : \n\n"\
                "User Name : {} ".format(issue_obj.assigned_to.name)+'\n'+\
                "Workspace: {} ".format(issue_obj.workspace.name)+'\n'+\
                "Task Name: {} ".format(issue_obj.title)+'\n'+\
                "Previous Status: {} ".format(prev_status)+'\n'+\
                "Present Status: {} ".format(aftr_status)

        send_mail(
            subject,
            body,
            from_mail,
            [to_email],
            fail_silently=False,
        )

        messages.success(request, 'Issue-status change success...')
    return HttpResponse('success')


def leave_status_change(request):

    if request.method == "GET" and request.is_ajax():
        leave_obj = Leave.objects.get(id=request.GET.get('id'),)
        leave_obj.leave_status = request.GET.get('leave_status',)
        Notification.objects.create(staff_mem=leave_obj.user, title='leave status has been updated', content=leave_obj.descritpion + ' has been ' + request.GET.get('leave_status',) + 'which is applied on '+ leave_obj.created_on)
        
        leave_obj.save()
        messages.success(request, 'Leave status changed...')
        return redirect('/attendance/')