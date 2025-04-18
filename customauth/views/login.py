import logging
import uuid
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site

from customauth.models import User
from customauth.forms import LoginForm, ForgotPasswordForm, SetPasswordForm
from customauth.send_mail import send_confirmation_email, send_password_reset_email

logger = logging.getLogger(__name__)


class LoginView(LoginView):
    """ Custom login view """
    template_name = 'customauth/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:dashboard')
        form = self.form_class
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        next_page = request.GET.get('next', '')
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user:
                if not user.verified_email:
                    # Generate new token
                    user.email_token = get_random_string(length=64)
                    user.save()

                    # Create confirmation link
                    confirmation_link = request.build_absolute_uri(
                        reverse('customauth:set_password', args=[user.email_token])
                    )

                    # Send confirmation email
                    send_confirmation_email(confirmation_link, user)

                    messages.warning(request, 'Your email is not verified. A new confirmation link has been sent to your email.')
                    return render(request, self.template_name, {'form': form})

                # Email is verified — login user
                login(request, user)
                return redirect(next_page or 'dashboard:dashboard')
            else:
                messages.warning(request, 'Invalid email or password')
        else:
            logger.error(f'Invalid form data: {form.errors}')
            messages.warning(request, 'Invalid email or password. Please enter correctly.')

        return render(request, self.template_name, {'form': form})


class ForgotPasswordView(View):
    template_name = "customauth/forgot_password.html"
    form_class = ForgotPasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)

            if users.exists():
                for user in users:
                    token = str(uuid.uuid4())

                    user.email_token = token
                    user.save()

                    reset_path = reverse_lazy('customauth:set_password', kwargs={
                        'token': token,
                    })

                    domain = get_current_site(request).domain
                    reset_link = f"https://{domain}{reset_path}"

                    send_password_reset_email(reset_link, user)

                messages.success(request, "Password reset email has been sent.")
            else:
                messages.error(request, "No account found with that email address.")

            return redirect('customauth:forgot_password')

        return render(request, self.template_name, {'form': form})


class SetNewPasswordView(View):
    template_name = "customauth/set_password.html"
    form_class = SetPasswordForm

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')  # Assuming the token is passed in the URL
        try:
            user = User.objects.get(email_token=token)  # Get the user by ID
            
            # Verify token
            if token == user.email_token:
                form = self.form_class()
                context = {
                    'form': form,
                    'token': token,
                }
                return render(request, self.template_name, context)
            else:
                messages.error(request, "Invalid or expired token.")
                return redirect('customauth:login')
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('customauth:login')

    def post(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            user = User.objects.get(email_token=token)

            # Verify token again
            if token == user.email_token:
                form = self.form_class(request.POST)
                if form.is_valid():
                    # Set the new password
                    new_password = form.cleaned_data['password']
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Your password has been reset successfully.")
                    return redirect('customauth:login')
                else:
                    context = {
                        'form': form,
                        'token': token,
                    }
                    return render(request, self.template_name, context)
            else:
                messages.error(request, "Invalid or expired token.")
                return redirect('customauth:login')
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('customauth:login')