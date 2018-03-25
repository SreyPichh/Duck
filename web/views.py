import logging
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from .forms import SignupForm

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        logging.debug("METHO POST")
        logging.debug("------------------------")
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate you account.'
            message = render_to_string('account_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_decode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get(email)
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.sand()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form':form})
#create activate Function
#this function will check token if it valid then user will activ and login
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverFlowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        #return redirect home
        return HttpResponse('Thank you for your email confirmation. Now you can login into you account.')
    else:
        return HttpResponse('Activate link is invalid!')
