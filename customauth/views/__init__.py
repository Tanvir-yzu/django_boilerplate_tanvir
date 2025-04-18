from .login import LoginView, ForgotPasswordView, SetNewPasswordView
from .logout import user_logout
from .profile import ProfileView, UserProfileView
from .register import RegisterView, confirm_email


__all__ = [
    LoginView,
    user_logout,
    RegisterView,
    ProfileView,
    UserProfileView,
    confirm_email,
    ForgotPasswordView,
    SetNewPasswordView,
]