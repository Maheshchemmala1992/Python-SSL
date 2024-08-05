from django.urls import path
from dashboard.views import dashboard_views as dash_views
from dashboard.views import api_views
from dashboard import helpers as helper_views
from dashboard.views import auth_views
from dashboard.views import workspace_views
# from attendance import views as attendance_views


urlpatterns = (

    path('', dash_views.home, name='home'),
    path('workspace/<int:id>/update', dash_views.workspace_edit, name='workspace-edit'),

    path('login', auth_views.login, name='login'),
    path('signup', auth_views.signup, name='signup'),
    path('logout', auth_views.logout, name='logout'),

    path('forgot/password', auth_views.forget_password, name='forget_password'),
    path('otp', auth_views.otp, name='otp'),
    path('reset/password', auth_views.reset_password, name='reset_password'),

    
    path('task-status', helper_views.tasK_status_change, name='task-status'),
    path('self-task-status', helper_views.self_tasK_status_change, name='self-task-status'),
    path('issue-status', helper_views.issue_status_change, name='issue-status'),
    path('leave-status', helper_views.leave_status_change, name='leave-status'),

    path('api/team', api_views.TeamView.as_view(), name='team-add'),
    path('api/task', api_views.TaskView.as_view(), name='task-add'),
    path('api/self-task', api_views.Self_TaskView.as_view(), name='self-task'),
    path('api/issue', api_views.IssueView.as_view(), name='issue-add'),
    path('api/work-space', api_views.WorkSpaceView.as_view(), name='work-space-add'),
    path('api/comment/task/<int:task_id>', api_views.TaskCommentView.as_view(), name='task-comment-add'),
    path('api/comment/issue/<int:issue_id>', api_views.IssueCommentView.as_view(), name='issue-comment-add'),


    path('<slug:name>', workspace_views.workspace_view, name='workspace'),
    path('<slug:workspace_slug>/<int:id>/task', workspace_views.task_detail_update_view, name='task-edit'),
    path('<slug:workspace_slug>/<int:id>/self-task', workspace_views.self_task_detail_update_view, name='self-task-edit'),
    path('<slug:workspace_slug>/<int:id>/issue', workspace_views.issue_detail_update_view, name='issue-edit'),
    path('<slug:workspace_slug>/<int:id>/self-email', workspace_views.self_task_email, name='self-email'),
    path('document_list', workspace_views.document_list, name='document_list'),

    path('<int:id>/task/delete', workspace_views.task_delete, name='task-delete'),
    path('<int:id>/self-task/delete', workspace_views.self_task_delete, name='self-task-delete'),
    path('<int:id>/issue/delete', workspace_views.issue_delete, name='issue-delete'),

    # attendace urls
    path('attendace/check-in', api_views.AttendanceInView.as_view(), name='attendance_check_in'),
    path('attendace/check-out', api_views.AttendaceOutView.as_view(), name='attendance_check_out'),

    path('leave/apply', api_views.LeaveView.as_view(), name='leave_apply'),
    path('holiday/', api_views.HolidayView.as_view(), name='holiday'),

    # path('holiday/<int:id>/delete', attendance_views.holiday_delete, name='holiday_delete'),

    path('notification/<int:id>', dash_views.notification_detailed_view, name='notification_detailed_view'),
    path('notifications/', dash_views.user_notofications_view, name='user_notofications_view'),
)