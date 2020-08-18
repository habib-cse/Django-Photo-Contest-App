from django.shortcuts import render,redirect
import hashlib,datetime
from django.contrib import messages 
from .models import User
from django.db.models import Max
from django.core.mail import send_mail
# Create your views here.

host = 'http://127.0.0.1:8000/'
admin_email = "habib41juwel@gmail.com"

def home(request):
    return render(request, 'frontend/index.html')

def user_login(request):
    if request.method == 'POST':
        useremail = request.POST['email']
        user_password = request.POST['password']
        enc_pass = hashlib.md5(user_password.encode())
        password = enc_pass.hexdigest()
        check_user = User.objects.filter(email=useremail, password = password)
        if check_user.exists():
            check_user = check_user.first()
            if not check_user.status:
                messages.warning(request, "Your account is temporarily suspended !!!")
                return redirect('core:login')
            else:
                request.session['user'] = check_user.id
                request.session['name'] = check_user.name
                return redirect('core:home') 
        else:
            messages.error(request,"Invalid Credential!!! Email or Password is not correct")
    return render(request, 'accounts/login-register.html')

def user_logout(request):
    request.session['user'] = None
    return redirect('core:login')

def user_registration(request):
    if request.method == 'POST':
        name = request.POST['user_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        max_id = User.objects.latest('id')  
        user_id = max_id.id + 100

        if password == password2:
            password = hashlib.md5(password.encode())
            encpass = password.hexdigest()
            check_user = User.objects.filter(email = email)
            if check_user.exists():
                check_user = check_user[0]
                if check_user.active_status:
                    messages.warning(request, "User already exists with this email")
                    return redirect('core:user_registration')
                else:
                    check_user.delete()
            
            user = User.objects.create(user_id=user_id,name=name,email=email,password=encpass)
            email_subject = "Phoconse - New Member Confirmation"
            user_tracking_id = str(user.id)
            user_id = hashlib.md5(user_tracking_id.encode())
            activation_key = user_id.hexdigest()
            user.activation_key = activation_key
            user.save() 
            user_active_link = host+"auth/activation/{}/".format(activation_key)
            email_msg = """
                <p>Thank you for joining Phoconse. Please confirm your membership. Click link visible below or copy-paste it in your browser.<br/> </p>
                <a target="_blank" href="{}">{}</a> 
               <p>After verification, you’ll have full access to your Phoconse account. <br/><br/></p>
                <p>Thank you,<br />
                Phoconse Team</p>
            """ .format(user_active_link,user_active_link) 
            send_mail(
                email_subject,
                email_msg,
                admin_email,
                [email],
                fail_silently=False, 
                html_message=email_msg, 
            ) 
            messages.success(request,"Account Created Successfully. Please check your email to active your account")
            return redirect('core:user_registration')
        else:
            messages.error(request, "Password Doesn't Matched")
    return render(request, 'accounts/login-register.html')

def user_active(request, value): 
    user = User.objects.get(activation_key=value)
    user.active_status = True
    user.status = True
    user.save() 
    request.session['user'] = user.id
    request.session['name'] = user.name
    return render(request,'accounts/account_activated_successfully.html')

def forgot_password(request):
    if request.method== 'POST':
        user_email = request.POST['email']
        user = User.objects.filter(email = user_email)
        if user.exists():
            user = user[0]
            email_subject = "Phoconse - Password reset"
            user_active_link = host+"auth/password-reset/{}/".format(user.activation_key)
            email_msg = """
                <p>Please confirm your membership. Click link visible below or copy-paste it in your browser to reset your password.<br/> </p>
                <a target="_blank" href="{}">{}</a>  
                <p>Thank you,<br />
                Phoconse Team</p>
            """ .format(user_active_link,user_active_link) 
            send_mail(
                email_subject,
                email_msg,
                admin_email,
                [user_email],
                fail_silently=False, 
                html_message=email_msg, 
            ) 
            messages.success(request,"Please check your email for a message with your password reset link")
        else:
            messages.error(request, "Your search did not return any Email. Please try again with valid Email.")
    return render(request,'accounts/forgot_password.html' )

def password_reset(request, value):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2'] 
        if password == password2:
            password = hashlib.md5(password.encode())
            encpass = password.hexdigest()
            check_user = User.objects.filter(activation_key = value).update(password=encpass)
            messages.success(request, "Your Password is changed successfully.")
            return redirect('core:login')
        else:
            messages.success(request, "Password do not matched")
    return render(request,'accounts/password_reset.html')




def gallery_list(request):
    return render(request, 'frontend/gallery_list.html')