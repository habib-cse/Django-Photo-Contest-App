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
            email_subject = "Active your Phoconse Account"
            user_active_link = host+"phoconse/new-user-account-activate/{}/active".format(user.id)
            email_msg = """
                <p><strong>Hello {},</strong> <br> 
                Click the following link to Active Your Phoconse Account <br>
                <a target="_blank" href="{}">{}</a> 
            """ .format(user.name,user_active_link,user_active_link) 
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

def user_active(request, id):
    print(id)
    user = User.objects.get(id=id)
    user.active_status = True
    user.status = True
    user.save()
    messages.success(request, "Congratulation!! your account is active now.")
    return redirect('core:user_registration')


def gallery_list(request):
    return render(request, 'frontend/gallery_list.html')


def gallery_individual(request, id):
    return render(request, 'frontend/gallery_individual.html')