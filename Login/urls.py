from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('logout', views.logoutuser, name="logout"),
    path('loginuser', views.loginuser, name='loginuser'),
    path('account', views.Account, name="account"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    # reseting ang changing the password
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name ="Login/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name ="Login/password_reset_done.html"), name="password_reset_complete"),
    path('reset_password', views.password_reset_request, name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name ="Login/password_reset_sent.html"),name="password_reset_done"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='Login/html screens/password_change_done.html'), 
        name='password_change_done'),
    path('password_change', auth_views.PasswordChangeView.as_view(template_name='Login/html screens/password_change.html'), name="password_change"),
]