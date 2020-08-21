from django.urls import path 
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.home,name="home"),
    path('phoconse/login',views.user_login,name="login"),
    path('phoconse/logout',views.user_logout,name="user_logout"),
    path('phoconse/register',views.user_registration,name="user_registration"),
    path('phoconse/new-user-account-activate/<int:id>/active',views.user_active,name="user_active"),
    path('phoconse/gallery-list',views.gallery_list,name="gallery_list"),
    path('phoconse/gallery/<int:id>',views.gallery_individual,name="gallery_individual"),
    path('phoconse/judge-list',views.judge_list,name="judge_list"),
    path('phoconse/judge/<int:id>',views.single_judge,name="single_judge"),
    path('phoconse/photo-contest',views.photo_contest,name="photo_contest"),
    path('phoconse/blog-list',views.blog_list,name="blog_list"),
    path('phoconse/blog/<int:id>',views.single_blog,name="single_blog"),
    path('phoconse/update-profile/<int:id>',views.update_profile,name="update_profile"),
    path('phoconse/about-us',views.about_us,name="about_us"),
    path('phoconse/contest-detail/<int:id>',views.contest_detail,name="contest_detail"),
    path('phoconse/contact',views.contact_us,name="contact_us"),
    path('phoconse/privacy-policy',views.privacy_policy,name="privacy_policy"),
    path('phoconse/trums-condition',views.trums_condition,name="trums_condition"),

]
