from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import SignUpView, password_reset_request, logOff, logIn


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logoff/', logOff, name='logoff'),
    url(r'login$', logIn, name='login'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/pwdreset_form.html',
             subject_template_name='registration/pwdreset_subject.txt',
             email_template_name='registration/pwdreset_email.html',
             success_url='login'
         ),
         name='password_reset'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/pwdreset_confirm.html',
             success_url='password_reset_complete'),
         name='password_reset_confirm'),

    url(r'password_reset_complete$',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/pwdreset_complete.html'),
         name='password_reset_complete'),
]
