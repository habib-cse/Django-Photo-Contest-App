from django.urls import path 
from . import views

app_name = 'core'

urlpatterns = [
    path('phoconse/login',views.user_login,name="login"),
    path('phoconse/register',views.user_registration,name="user_registration"),
    path('phoconse/new-user-account-activate/<int:id>/active',views.user_active,name="user_active"),
]
