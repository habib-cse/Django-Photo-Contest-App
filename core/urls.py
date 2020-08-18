from django.urls import path 
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.home,name="home"),
<<<<<<< HEAD
    path('auth/login',views.user_login,name="login"),
    path('auth/logout',views.user_logout,name="user_logout"),
    path('auth/register',views.user_registration,name="user_registration"),
    path('auth/activation/<str:value>/',views.user_active,name="user_active"),
    path('auth/forgotten-password/',views.forgot_password,name="forgot_password"),
    path('auth/password-reset/<str:value>/',views.password_reset,name="password_reset"),
    path('gallery-list',views.gallery_list,name="gallery_list"),
=======
    path('phoconse/login',views.user_login,name="login"),
    path('phoconse/logout',views.user_logout,name="user_logout"),
    path('phoconse/register',views.user_registration,name="user_registration"),
    path('phoconse/new-user-account-activate/<int:id>/active',views.user_active,name="user_active"),
    path('phoconse/gallery-list',views.gallery_list,name="gallery_list"),
    path('phoconse/gallery/<int:id>',views.gallery_individual,name="gallery_individual"),
>>>>>>> dev

]
