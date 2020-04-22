from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic
from rest_framework import authentication, generics, permissions
from rest_framework.response import Response

from .forms import SignUpForm
from .tokens import user_activation_token

User = get_user_model()


class SignupView(generic.View):
    def get(self, *args, **kwargs):
        form = SignUpForm()
        return render(self.request, 'registration/signup.html', {'form': form})

    def post(self, *args, **kwargs):
        form = SignUpForm(self.request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(self.request)
            subject = 'Activate Your Library Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
        else:
            if form.errors:
                messages.error(self.request, form.errors)
            else:
                messages.error(self.request, "Time out")

            form = SignUpForm()
            return render(self.request, 'registration/signup.html', {'form': form})


class AccountActicationSent(generic.View):
    def get(self, *args, **kwargs):
        return render(self.request, 'registration/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('books:book_list')
    else:
        return render(request, 'registration/account_activation_invalid.html')


class UserDetailAPIView(generics.views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.SessionAuthentication]

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = {
                'id': self.request.user.id,
                'username': self.request.user.username,
                'email': self.request.user.email
            }
            if self.request.user.is_staff:
                user['role'] = 'staff'
            else:
                user['role'] = 'user'

        else:
            user = {
                'id': None,
                'username': 'guest',
                'email': None,
                'role': 'guest'
            }

        return Response(user)