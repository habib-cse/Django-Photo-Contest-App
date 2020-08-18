from django.urls import path 
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.home,name="home"),
    path('phoconse/login',views.user_login,name="login"),
    path('phoconse/logout',views.user_logout,name="user_logout"),
    path('phoconse/register',views.user_registration,name="user_registration"),
    path('phoconse/new-user-account-activate/<int:id>/active',views.user_active,name="user_active"),
]
