from django.contrib import messages
from django.core import exceptions
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from dashboard.models import *
from dashboard.forms import *
from dashboard.views.dashboard_views import is_authenticated

from django.core.mail import send_mail
from django.conf import settings
import random


def login(request):

    login_obj = ''
    login_check = ''
    
    if request.method == 'POST':
        e = ''
        email_input = request.POST.get('email_temp')
        pwd = request.POST.get('pass_temp')

        try:
            try:
                login_obj = StaffUser.objects.get(name=email_input).email
            except:
                login_obj = StaffUser.objects.get(email=email_input)
        except Exception as e:
            pass

        if login_obj != '':
            e = ''
            try:
                try:
                    login_check = StaffUser.objects.get(name=email_input, password=pwd)
                except:
                    login_check = StaffUser.objects.get(email=email_input, password=pwd)

                if login_check:
                    request.session['id'] = login_check.id
                    request.session['user_name'] = login_check.name
                    request.session['is_admin'] = login_check.is_admin
                    messages.success(request, 'You are successfully logged-in.')
                    return redirect('home')
            except Exception as e:
                print('-exception as error in login---', e)
                messages.error(request, 'Invalid Password..!')
        else:
            messages.error(request, 'Please check email or user-name...!')
    team_list = Team.objects.filter(status=True)
    return render(request, 'dashboard/login.html', {'teams':team_list})


@is_authenticated
def logout(request):

    try:
        del request.session['id']
        del request.session['user_name']
        messages.success(request, 'Logout Successfully...!')
    except Exception as e:
        print('-exception error in logout---', e)
        pass

    return redirect('login')


def signup(request):

    if request.method == 'POST':
        try:
            if len(User.objects.filter(username=request.POST['name'])) > 0:
                messages.error(request, 'provided user name already taken..')
            elif len(User.objects.filter(email=request.POST['email'])) > 0:
                messages.error(request, 'Provided Email already taken..')
            else:
                form = StaffUserForm(request.POST)
                if form.is_valid():
                    form_save = form.save(commit = False)
                    user = User.objects.create_user(username=request.POST['name'], email=request.POST['email'], password=request.POST['password'])
                    form_save.user_id = user
                    form_save.save()

                    from_mail = settings.EMAIL_HOST_USER
                    to_email = form_save.email
                    body = "DITS staff acccount has been created: \n\n"\
                            "User Name : {} ".format(form_save.name)+'\n'+\
                            "Email: {} ".format(form_save.email)+'\n'+\
                            "Password: {} ".format(form_save.password)+'\n'+\
                            "link: {} ".format('https://management.divsolution.com/login?name='+form_save.name+'&pwd='+form_save.password)

                    send_mail(
                        'Welcome to DITS Task Management App',
                        body,
                        from_mail,
                        [to_email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Member ' + form_save.name + ' added successfully...!')
                    return redirect('login')
        except Exception as e:
            print('----error as e----', e)
            messages.error(request, 'Provided user already exists..')
    else:
        form = StaffUserForm()
    return render(request, 'dashboard/login.html')
    

def forget_password(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        users = StaffUser.objects.filter(email=email)
        if len(users):
            user = users.last()
            request.session['email'] = user.email
            request.session['username'] = user.name
            otp = random.randint(10000, 99999)
            request.session['otp'] = otp
            request.session.set_expiry(300)
            subject = 'OTP Requested for forgot password'
            message = "We received a forgot password request from your account.\nMake sure not to share your OTP with anyone.\nOTP :{}.\nlink: {}. \n\n\nplease verify your account if it's not you".format(str(otp), 'https://management.divsolution.com/otp?otp='+str(otp))
            from_email = 'info@divsolution.com'

            send_mail(subject, message, from_email,
                      [email], fail_silently=False)
            return redirect('otp')
        else:
            messages.error(request, 'Enter a valid Registered Email..!')
            message = 'Enter a valid Registered Email..!'

    return render(request,'dashboard/forget_password.html')


def otp(request):

    session_otp = request.session.get('otp')
    if request.method == 'POST':
        otp = request.POST['otp']
        if int(session_otp) == int(otp):
            del request.session['otp']
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP, try again')
    return render(request, 'dashboard/otp.html')



def reset_password(request):

    try:
        user_obj = User.objects.get(email=request.session['email'])
        staff_obj = StaffUser.objects.get(email=request.session.get('email'))
    except:
        # messages.error(request, 'Your session timed out....!')
        response = '<script>alert("Your session times out...!");window.location.replace("https://management.divsolution.com/login")</script>'
        return HttpResponse(response)

    if request.method == 'POST':
        email = user_obj.email
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user_obj.set_password(password)
            user_obj.save()
            staff_obj.password = password
            staff_obj.save()

            subject = request.session['username'].capitalize(
            ) + "Your Password reset"
            
            message = 'Please find your account details below with credentials after password reset \nEmail :{}\nUser Name :{}\nPassword :{}\nLink: {}'.format(
                email.lower(), request.session['username'], str(password), 'https://management.divsolution.com/login')
            from_email = 'ditstaskmanager@gmail.com'
            send_mail(
                subject,
                message,
                from_email,
                [email],
                fail_silently=False,
            )
            del request.session['username']
            return redirect('login')
        else:
            messages.error(request, 'passwords mis-match')

    return render(request,'dashboard/reset_password.html')
