from django import forms


class ForgotPasswordForm(forms.Form):
    """ Form for requesting password reset """
    email = forms.CharField(
        label="Email",
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-400 text-white placeholder-gray-500',
            'name': 'email',
            'placeholder': 'you@example.com',
            'autofocus': True,
        })
    )


class SetPasswordForm(forms.Form):
    """ Form for setting a new password """
    password = forms.CharField(
        label="New Password",
        max_length=30,
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-400 text-white placeholder-gray-500',
            'name': 'password',
            'placeholder': '**********',
        })
    )
    confirm_password = forms.CharField(
        label="Confirm New Password",
        max_length=30,
        widget=forms.PasswordInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-400 text-white placeholder-gray-500',
            'name': 'confirm_password',
            'placeholder': '**********',
        })
    )