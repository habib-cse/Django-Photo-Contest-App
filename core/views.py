from django.shortcuts import render,redirect
import hashlib,datetime
from django.contrib import messages 
from .models import User,Gallery, Contest,Judge, Judgecat, Contestimg, Copyright
from django.db.models import Max
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from.forms import ContestimgForm
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
        total_user = User.objects.all().count()
        if total_user > 0:
            max_id = User.objects.latest('id')  
            user_id = max_id.id + 101
        else:
            user_id = 101

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
            
            user = User.objects.create(custom_user_id=user_id,name=name,email=email,password=encpass)
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
    if request.method== "POST":
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


def add_image(request, id):
    userid = request.session['user'] 
    form =  ContestimgForm() 
    if request.method == "POST": 
        form = ContestimgForm(request.POST, request.FILES)
        total_image = Contestimg.objects.all().count()
        if total_image > 0:
            max_id = Contestimg.objects.latest('id')  
            photo_id = max_id.id + 101
        else:
            photo_id = 101

        if form.is_valid(): 
            new_image = form.save(commit=False)   
            new_image.photo_id = photo_id
            new_image.user_id = userid
            new_image.save()
            messages.success(request,"Photo Uploaded Successfully")
            return redirect('core:add_image', userid) 

    context = {
        'form':form,
    }
    return render(request, 'frontend/add_image.html',context)


# def add_image(request, id):
#     userid = request.session['user']
#     contest_list = Contest.objects.filter(tags="Ongoing")
#     if request.method == "POST":
#         profile_pic = request.FILES.get('profile_pic')  

#         if profile_pic: 
#             fs = FileSystemStorage()
#             fname = fs.save(profile_pic.name, profile_pic)
#             upload_file_url = fs.url(fname)  

#         title = request.POST['title']
#         contest_id = int(request.POST['contest']) 
#         total_image = Contestimg.objects.all().count()
#         if total_image > 0:
#             max_id = Contestimg.objects.latest('id')  
#             photo_id = max_id.id + 101
#         else:
#             photo_id = 101

#         Contestimg.objects.create(photo_id=photo_id, contest_id=contest_id, image=profile_pic,image_title=title, user_id=userid)
#         messages.success(request,"Photo Uploaded Successfully") 

#     context = {
#         'contest_list':contest_list
#     }
#     return render(request, 'frontend/add_image.html',context)













def gallery_list(request):
    gallery_list = Gallery.objects.filter(status=True)
    total_gallery = gallery_list.count()
    context = {
        'gallery_list':gallery_list,
        'total_gallery':total_gallery
    }
    return render(request, 'frontend/gallery_list.html',context)


def gallery_individual(request, id): 
    ent1_image = False
    ent2_image = False
    ent3_image = False
    ent4_image = False
    ent5_image = False
    ent6_image = False
    ent7_image = False
    ent8_image = False
    ent9_image = False
    ent10_image = False
    ent11_image = False
    ent12_image = False
    ent13_image = False
    ent14_image = False
    ent15_image = False
    ent16_image = False
    ent17_image = False
    ent18_image = False
    ent19_image = False
    ent20_image = False
    ent21_image = False
    ent22_image = False
    ent23_image = False
    ent24_image = False
    ent25_image = False
    gallery = Gallery.objects.get(id=id)
    first_id = gallery.first_place_photo_id
    first_image = Contestimg.objects.get(photo_id=first_id)
    second_id = gallery.second_place_photo_id
    second_image = Contestimg.objects.get(photo_id=second_id)
    third_id = gallery.third_place_photo_id
    third_image = Contestimg.objects.get(photo_id=third_id) 
    if gallery.best_entry1_id:
        ent1_id = gallery.best_entry1_id
        ent1_image = Contestimg.objects.get(photo_id=ent1_id)

    if gallery.best_entry2_id:
        ent2_id = gallery.best_entry2_id
        ent2_image = Contestimg.objects.get(photo_id=ent2_id)
        
    if gallery.best_entry3_id:
        ent3_id = gallery.best_entry3_id
        ent3_image = Contestimg.objects.get(photo_id=ent3_id)

    if gallery.best_entry4_id:
        ent4_id = gallery.best_entry4_id
        ent4_image = Contestimg.objects.get(photo_id=ent4_id)

    if gallery.best_entry5_id:
        ent5_id = gallery.best_entry5_id
        ent5_image = Contestimg.objects.get(photo_id=ent5_id)

    if gallery.best_entry6_id:
        ent6_id = gallery.best_entry6_id
        ent6_image = Contestimg.objects.get(photo_id=ent6_id)

    if gallery.best_entry7_id:
        ent7_id = gallery.best_entry7_id
        ent7_image = Contestimg.objects.get(photo_id=ent7_id)

    if gallery.best_entry8_id:
        ent8_id = gallery.best_entry8_id
        ent8_image = Contestimg.objects.get(photo_id=ent8_id)

    if gallery.best_entry9_id:
        ent9_id = gallery.best_entry9_id
        ent9_image = Contestimg.objects.get(photo_id=ent9_id)

    if gallery.best_entry10_id:
        ent10_id = gallery.best_entry10_id
        ent10_image = Contestimg.objects.get(photo_id=ent10_id)
        
    if gallery.best_entry11_id:
        ent11_id = gallery.best_entry11_id
        ent11_image = Contestimg.objects.get(photo_id=ent11_id)
        
    if gallery.best_entry12_id:
        ent12_id = gallery.best_entry12_id
        ent12_image = Contestimg.objects.get(photo_id=ent12_id)
        
    if gallery.best_entry13_id:
        ent13_id = gallery.best_entry13_id
        ent13_image = Contestimg.objects.get(photo_id=ent13_id)
        
    if gallery.best_entry14_id:
        ent14_id = gallery.best_entry14_id
        ent14_image = Contestimg.objects.get(photo_id=ent14_id)
        
    if gallery.best_entry15_id:
        ent15_id = gallery.best_entry15_id
        ent15_image = Contestimg.objects.get(photo_id=ent15_id)
        
    if gallery.best_entry16_id:
        ent16_id = gallery.best_entry16_id
        ent16_image = Contestimg.objects.get(photo_id=ent16_id)
        
    if gallery.best_entry17_id:
        ent17_id = gallery.best_entry17_id
        ent17_image = Contestimg.objects.get(photo_id=ent17_id)
        
    if gallery.best_entry18_id:
        ent18_id = gallery.best_entry18_id
        ent18_image = Contestimg.objects.get(photo_id=ent18_id)
        
    if gallery.best_entry19_id:
        ent19_id = gallery.best_entry19_id
        ent19_image = Contestimg.objects.get(photo_id=ent19_id)
        
    if gallery.best_entry20_id:
        ent20_id = gallery.best_entry20_id
        ent20_image = Contestimg.objects.get(photo_id=ent20_id)
        
    if gallery.best_entry11_id:
        ent21_id = gallery.best_entry11_id
        ent21_image = Contestimg.objects.get(photo_id=ent21_id)
        
    if gallery.best_entry11_id:
        ent22_id = gallery.best_entry11_id
        ent22_image = Contestimg.objects.get(photo_id=ent22_id)
        
    if gallery.best_entry11_id:
        ent23_id = gallery.best_entry11_id
        ent23_image = Contestimg.objects.get(photo_id=ent23_id)
        
    if gallery.best_entry11_id:
        ent24_id = gallery.best_entry11_id
        ent24_image = Contestimg.objects.get(photo_id=ent24_id)

    if gallery.best_entry25_id:
        ent25_id = gallery.best_entry25_id
        ent25_image = Contestimg.objects.get(photo_id=ent25_id)

    context = {
        'gallery':gallery,
        'first_image':first_image,
        'second_image':second_image,
        'third_image':third_image,
        'ent1_image':ent1_image,
        'ent2_image':ent2_image,
        'ent3_image':ent3_image,
        'ent4_image':ent4_image,
        'ent5_image':ent5_image,  
        'ent6_image':ent6_image,  
        'ent7_image':ent7_image,  
        'ent8_image':ent8_image,  
        'ent9_image':ent9_image,  
        'ent10_image':ent10_image,  
        'ent11_image':ent11_image,  
        'ent12_image':ent12_image,  
        'ent13_image':ent13_image,  
        'ent14_image':ent14_image,  
        'ent15_image':ent15_image,  
        'ent16_image':ent16_image,  
        'ent17_image':ent17_image,  
        'ent18_image':ent18_image,  
        'ent19_image':ent19_image,  
        'ent20_image':ent20_image,  
        'ent21_image':ent21_image,  
        'ent22_image':ent22_image,  
        'ent23_image':ent23_image,  
        'ent24_image':ent24_image,  
        'ent25_image':ent25_image,
    }
    return render(request, 'frontend/gallery_individual.html',context)


