from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # Authentication
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("accounts/login/", views.CustomLoginView.as_view(), name="account_login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("accounts/logout/", views.LogoutView.as_view(), name="account_logout"),

    # Password Management
    path("accounts/password_new/",
         views.UserPasswordSetView.as_view(), name="password_new"),
    path("accounts/password_change/",
         views.PasswordChangeView.as_view(), name="password_change"),
    path("accounts/password_change/done/",
         views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("accounts/password_reset/",
         views.PasswordResetView.as_view(), name="password_reset"),
    path("accounts/password_reset/done/",
         views.PasswordResetKeyDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/",
         views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/reset/completed/", views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path("accounts/reset/invalid/", views.PasswordResetInvalidView.as_view(),
         name="password_reset_invalid"),

    # Email Verification
    path("accounts/verify_email/", views.signup_verify_email, name="verify_email"),
    path("accounts/verify_email/sent/",
         views.RegisterEmailValidationSentView.as_view(), name="verify_email_sent"),
    path("accounts/verify_email/resend/",
         views.resend_verification_email, name="verify_email_resend"),
    path("accounts/verify_email_change/",
         views.verify_email_change, name="verify_email_change"),

    # Profile
    path("accounts/profile/", views.ProfileView.as_view(), name="profile"),
    path("accounts/profile/edit/",
         views.ProfileEditView.as_view(), name="profile_edit"),
    path("accounts/profile/edit/email/",
         views.ProfileEmailEditView.as_view(), name="profile_edit_email"),

    # Signup
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("signup/email/", views.SignupEmailView.as_view(), name="signup_email"),
    path("signup/username/", views.SignupUsernameView.as_view(),
         name="signup_username"),
]
