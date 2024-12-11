from django.urls import path
from user_account.views import *

urlpatterns = [
    path('',home,name='home'),
    path('login',login_page,name='login-url'),
    path('signup',signup_page,name='signup-url'),
    path('logout',logout_user,name='logout-url'),
    path('user_home',user_homepage,name='user-homepage-url'),
]