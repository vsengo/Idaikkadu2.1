# accounts/views.py
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views import generic
from accounts.forms import RegisterForm


class SignUpView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def logOff(request):
    logout(request)
    user = User.objects.filter(username=request.user)
    return render(request, 'registration/logoff.html',{'user':user})

def logIn(request):
    return render(request, 'registration/login.html')

#Unused
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid( ):
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists( ):
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/pwdreset_subject.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Idaikkadu.com',
                        "uid": urlsafe_base64_encode(force_bytes(user.username)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'accounts@idaikkadu.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    return render(request, 'registration/pwdreset_email.html',{'user':user})

    password_reset_form = PasswordResetForm( )
    return render(request=request, template_name="registration/pwdreset_form.html",context={"password_reset_form": password_reset_form})