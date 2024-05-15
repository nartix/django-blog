from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import (
    login as auth_login,
    get_user_model,
    update_session_auth_hash,
)
from django.contrib import messages
from django.utils.http import (
    url_has_allowed_host_and_scheme as is_safe_url,
    urlsafe_base64_encode,
)
from django.utils.translation import gettext as _
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import SignatureExpired, BadSignature
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.middleware import csrf as CsrfViewMiddleware
from django import forms
import logging

from django.conf import settings

from users.forms import (
    CustomUserCreationForm,
    PasswordResetUsernameEmailForm,
    UserSetPasswordForm,
    UserEditForm,
    EmailForm,
    UsernameForm,
    ProfileEmailEditForm,
)
from core.mixins import CoreMixin
from users.mixins import UnauthenticatedUserMixin, ResetTokenValidationMixin
from core.tasks import send_email_task
from users.models import UnverifiedUser
from users.utils import create_signed_user_token, UserAuthManager
from core.utils import Tokenizer, encode_base64_key, decode_base64_key

User = get_user_model()


logger = logging.getLogger("core")


class CustomLoginView(CoreMixin, LoginView):
    # template_name = "users/login.html"  # Default template
    template_name = "core/form/form_minimum.html"
    redirect_authenticated_user = True
    title = _("Sign in to your account")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "")
        context["action_url"] = reverse_lazy("users:login")
        context["button_text"] = _("Login")
        context["form_type"] = "login"
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["username"].label = _("Username or Email")
        return form

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        self.request.session["auth_method"] = "password"

        next_url = self.request.POST.get("next")
        if next_url and is_safe_url(next_url, allowed_hosts={self.request.get_host()}):
            return HttpResponseRedirect(next_url)

        return redirect("core:index")

    def form_invalid(self, form):
        messages.error(self.request, _("Invalid username or password."))
        form.data = form.data.copy()
        form.data["password"] = ""
        return super().form_invalid(form)


class LogoutView(LogoutView):
    next_page = reverse_lazy("core:index")


class SignupView(UnauthenticatedUserMixin, CoreMixin, FormView):
    form_class = CustomUserCreationForm
    template_name = "core/form/form_minimum.html"
    email_template_name = "users/email/registration_email_validation_message.txt"
    success_url = reverse_lazy("users:verify_email_sent")
    title = _("Sign Up")

    def form_valid(self, form):
        # user = form.save()
        email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password1")

        unverified_user, created = UserAuthManager.update_or_create_unverified_user(
            username, email, raw_password)

        logger.info(f"Unverified user created: {unverified_user}")

        # Proceed to send a verification email
        self.send_verification_email(unverified_user)

        return super().form_valid(form)

        # if ever disabled email verification
        # user = authenticate(username=username, password=raw_password)
        # if user is not None:
        #     auth_login(self.request, user)
        # return super().form_valid(form)

    def send_verification_email(self, user):
        context = {
            "user": user,
            "protocol": "https" if self.request.is_secure() else "http",
            "domain": get_current_site(self.request).domain,
            "site_name": get_current_site(self.request).name,
            "uid": encode_base64_key(user.pk),
            "token": Tokenizer().encode(user.pk, user.username, user.email, user.password, user.date_joined),
        }

        subject = _("Verify your email address")
        message = render_to_string(self.email_template_name, context)

        # Store email data in session
        self.request.session["email_data"] = {
            "subject": subject,
            "message": message,
            "recipient_list": [user.email],
            "username": user.username,
        }

        send_email_task.delay(subject, message, [user.email])
        logger.info(
            f"Verification email sent to {user.username} at {user.email}")

    def form_invalid(self, form):
        if "username" in form.cleaned_data:
            self.show_success_message = True

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "validation_check": ["username", "email"],
                "show_success_message": getattr(self, "show_success_message", False),
                "action_url": reverse_lazy("users:signup"),
                "button_text": _("Sign Up"),
                "form_type": "signup",
            }
        )
        return context


def resend_verification_email(request):
    try:
        if not request.headers.get("HX-Request") or request.method != "POST":
            return HttpResponse(_(""))

        email_data = request.session.get("email_data")

        if email_data is not None:
            send_email_task.delay(
                email_data["subject"],
                email_data["message"],
                email_data["recipient_list"],
            )
            del request.session["email_data"]
            logger.info(
                f"Verification email resent to {email_data['recipient_list']} for {email_data['username']}"
            )

        return HttpResponse(_("Email has been sent again."))
    except CsrfViewMiddleware.CsrfFailure:
        # Handle the CSRF token error here
        return HttpResponse(_("CSRF token error occurred."))


class RegisterEmailValidationSentView(CoreMixin, TemplateView):
    template_name = "users/registration/registration_email_validation_sent.html"
    title = _("Email Validation Sent")


def signup_verify_email2(request):
    token = request.GET.get("token")
    id = request.GET.get("id")

    try:
        pk = decode_base64_key(id)
        user = UserAuthManager.get_unverified_user_by_pk(pk)
        # Attempt to unsign the token within 3 days
        token_user = Tokenizer().decode(user.pk, user.username, user.email, user.password, user.date_joined,
                                        token=token, max_age=settings.PASSWORD_RESET_TIMEOUT
                                        )

        # For scenario where user registers the same email using OAuth
        # before verifying the email
        if (UserAuthManager.do_email_pk_exist(
                    user.pk, user.email)
                ):
            messages.error(request, _(
                "Email already registered. Please login."))
            return redirect("users:login")

        # The token is valid, and proceed with activating the user account
        unverified_user = user
        if unverified_user:
            # For scenario where username gets taken while user is verifying email
            # Check if username already exists in User model
            username = unverified_user.username
            count = 1
            while UserAuthManager.does_username_exist(username):
                # Append a number to the end of the username
                username = f"{unverified_user.username}{count}"
                count += 1

            UserAuthManager.create_user(
                username=username,
                email=unverified_user.email,
                password=unverified_user.password,
                email_verified=True,
                username_editable=True if count > 1 else False
            )

            logger.info(
                f"User created with username: {username} after email verification."
            )

            # Delete the unverified user
            unverified_user.delete()

            messages.success(
                request, _("Your email has been verified. You can now login.")
            )
            return redirect("users:login")
        else:
            # Handle the case where the email does not exist in the UnverifiedUser model
            messages.error(
                request, _("Invalid or expired token. Please sign up again.")
            )
            logger.error(f"Invalid or expired email verification token")
            return redirect("users:signup")

    except SignatureExpired:
        messages.error(request, _(
            "Your token has expired. Please sign up again."))
        logger.error(f"Expired email verification token")
        return redirect("users:signup")

    except BadSignature:
        # Handle the case for tampering or bad token
        logger.error(f"Invalid or tampered email verification token")
        messages.error(request, _("Invalid token. Please sign up again."))
        return redirect("users:signup")


def signup_verify_email(request):
    token = request.GET.get("token")
    id = request.GET.get("id")

    if not token or not id:
        messages.error(request, _("Invalid or missing token or user id."))
        logger.error(f"Missing token or user id in verification request")
        return redirect("users:signup")

    try:
        pk = decode_base64_key(id)
        user = UserAuthManager.get_unverified_user_by_pk(pk)
        # Directly attempt to unsign the token
        token_user = Tokenizer().decode(user.pk, user.username, user.email, user.password, user.date_joined,
                                        token=token, max_age=settings.PASSWORD_RESET_TIMEOUT)

        # Check if email already registered with another account
        if UserAuthManager.do_email_pk_exist(user.pk, user.email):
            messages.error(request, _(
                "Email already registered. Please login."))
            return redirect("users:login")

        # Generate a unique username if necessary
        username = user.username
        count = 1
        while UserAuthManager.does_username_exist(username):
            username = f"{user.username}{count}"
            count += 1

        # Create the user
        UserAuthManager.create_user(
            username=username,
            email=user.email,
            password=user.password,
            email_verified=True,
            username_editable=True if count > 1 else False
        )

        logger.info(
            f"User created with username: {username} after email verification.")
        user.delete()  # Delete the unverified user record

        messages.success(request, _(
            "Your email has been verified. You can now login."))
        return redirect("users:login")

    except SignatureExpired:
        messages.error(request, _(
            "Your token has expired. Please sign up again."))
        logger.error("Expired email verification token")
        return redirect("users:signup")

    except BadSignature:
        logger.error("Invalid or tampered email verification token")
        messages.error(request, _("Invalid token. Please sign up again."))
        return redirect("users:signup")


class SignupUsernameView(SignupView):
    template_name = "core/form/form_input_fields.html"
    form_class = UsernameForm

    def form_valid(self, form):
        context = self.get_context_data()
        context["show_success_message"] = True
        return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "validation_check": ["username"],
                "show_success_message": False,
            }
        )
        return context


class SignupEmailView(SignupView):
    template_name = "core/form/form_input_fields.html"
    form_class = EmailForm

    def form_valid(self, form):
        context = self.get_context_data()
        context["show_success_message"] = True
        return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "validation_check": ["email"],
                "show_success_message": False,
            }
        )
        return context


class PasswordChangeView(CoreMixin, PasswordChangeView):
    template_name = "core/form/form_minimum.html"
    # success_url = reverse_lazy("users:password_change_done")
    success_url = reverse_lazy("users:profile")
    title = _("Change Password")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = reverse("users:password_change")
        context["button_text"] = _("Change Password")
        return context

    def form_valid(self, form):
        messages.success(
            self.request, _("Your password has been changed successfully.")
        )
        return super().form_valid(form)


class PasswordChangeDoneView(CoreMixin, PasswordResetDoneView):
    template_name = (
        "users/registration/password_change_done.html"  # Path to your template
    )
    title = _("Password Change Successful")


class PasswordResetView(UnauthenticatedUserMixin, CoreMixin, PasswordResetView):
    template_name = "core/form/form_minimum.html"
    email_template_name = "users/email/password_reset_key_message.txt"
    # subject_template_name = 'users/registration/password_reset_subject.txt'
    success_url = reverse_lazy("users:password_reset_done")
    title = _("Forgot your password?")
    form_class = PasswordResetUsernameEmailForm

    def form_valid(self, form):
        username_or_email = form.cleaned_data.get("username_or_email")
        email = form.cleaned_data.get("email")

        try:
            if email:
                # If email is provided, get user by email
                user = UserAuthManager.get_user_by_email(email)
            else:
                # If email is not provided, but a username or email is provided in the username_or_email field, get by username
                user = UserAuthManager.get_user_by_username(username_or_email)

            if user.password:
                # If user has a password, proceed to send the password reset email
                # Social Account only logins won't have a password
                self.send_password_reset_email(user)
        except User.DoesNotExist:
            logger.error(
                f"Dummy password reset email sent message shown for {username_or_email}"
            )

        return HttpResponseRedirect(self.get_success_url())

    def send_password_reset_email(self, user):
        context = self.get_email_context(user)
        subject = render_to_string(self.subject_template_name, context).strip()
        message = render_to_string(self.email_template_name, context)
        send_email_task.delay(subject, message, [user.email])
        logger.info(f"Password reset email sent to {user.username}")

    def get_email_context(self, user):
        return {
            "email": user.email,
            "domain": get_current_site(self.request).domain,
            "site_name": get_current_site(self.request).name,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            "token": default_token_generator.make_token(user),
            "protocol": "https" if self.request.is_secure() else "http",
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_message"] = _(
            "Give us the email address or username you signed up with and we'll send you details on how to reset your password."
        )
        context["action_url"] = reverse("users:password_reset")
        context["button_text"] = _("Reset Your Password")
        return context


class PasswordResetConfirmView(
    ResetTokenValidationMixin, CoreMixin, PasswordResetConfirmView
):
    template_name = "core/form/form_minimum.html"
    success_url = reverse_lazy("users:password_reset_complete")
    title = _("Reset Password")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = reverse(
            "users:password_reset_confirm",
            kwargs={"uidb64": self.kwargs["uidb64"],
                    "token": self.kwargs["token"]},
        )
        context["button_text"] = _("Reset Password")
        return context


class PasswordResetInvalidView(CoreMixin, TemplateView):
    template_name = "users/registration/password_reset_invalid.html"
    title = _("Password Reset Invalid")


class PasswordResetCompleteView(CoreMixin, PasswordResetCompleteView):
    template_name = "users/registration/password_reset_complete.html"
    title = _("Password Reset Complete")


class PasswordResetKeyDoneView(CoreMixin, PasswordResetDoneView):
    template_name = "users/registration/password_reset_done.html"
    title = _("Password Reset Email Sent")


# create profile view class that use detailview, load user profile and pass it to the template


class ProfileView(CoreMixin, LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
    title = _("Profile")

    def get_context_data(self, **kwargs):
        logger.info("Auth method: " +
                    self.request.session.get("auth_method", ""))
        logger.info("Auth provider: " +
                    self.request.session.get("oauth_provider", ""))
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["uid_token"] = create_signed_user_token(user)

        linked_providers = user.oauth_accounts.values_list(
            "provider__name", flat=True)
        linked_accounts = user.oauth_accounts.values("provider__name", "email")
        oauth_users = {
            account["provider__name"]: account["email"] for account in linked_accounts
        }
        context["oauth_users"] = oauth_users

        context["is_google_linked"] = "google" in linked_providers
        context["is_microsoft_linked"] = "microsoft" in linked_providers

        # set next to the current url
        context["next"] = self.request.path
        return context


class UserPasswordSetView(LoginRequiredMixin, CoreMixin, FormView):
    template_name = "core/form/form_minimum.html"
    form_class = UserSetPasswordForm
    success_url = reverse_lazy("users:profile")
    title = _("Set New Password")

    def get_form_kwargs(self):
        kwargs = super(UserPasswordSetView, self).get_form_kwargs()
        kwargs["user"] = self.request.user  # Pass the current user to the form
        return kwargs

    # def form_valid(self, form):
    #     form.save()  # Save the new password
    #     messages.success(self.request, "Your password has been set successfully.")
    #     return super(UserPasswordSetView, self).form_valid(form)

    def form_valid(self, form):
        form.save()  # Save the new password
        update_session_auth_hash(
            self.request, form.user
        )  # Update the session with the new password hash
        messages.success(
            self.request,
            _(
                "Your password has been set successfully. You can now log in with your username or email and new password."
            ),
        )
        return super(UserPasswordSetView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = reverse("users:password_new")
        context["button_text"] = _("Set New Password")
        return context


class ProfileEditView(LoginRequiredMixin, CoreMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "core/form/form_minimum.html"
    # Redirect to a new URL after saving
    success_url = reverse_lazy("users:profile")
    title = _("Edit Profile")

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = reverse("users:profile_edit")
        context["button_text"] = _("Save Changes")
        return context


class ProfileEmailEditView(LoginRequiredMixin, CoreMixin, FormView):
    form_class = ProfileEmailEditForm
    template_name = "core/form/form_minimum.html"
    success_url = reverse_lazy("users:profile")
    title = _("Edit Email Address")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Pass the current user to the form
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial["email"] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data.get("email")

        if new_email.lower() != user.email.lower():
            user.email2 = new_email
            # Send a verification email to the new email address
            self.send_verification_email(user)
            messages.success(
                self.request,
                _("Please check your email to validate the new email address."),
            )
        else:
            # user email is the same as the new email
            if user.email2:
                user.email2 = ""

        user.save()
        return redirect(self.success_url)

    def send_verification_email(self, user):

        context = {
            "user": user,
            "protocol": "https" if self.request.is_secure() else "http",
            "domain": get_current_site(self.request).domain,
            "site_name": get_current_site(self.request).name,
            "uid": encode_base64_key(user.pk),
            "token": Tokenizer().encode(user.pk, user.email2, user.password, user.date_joined),
        }

        logger.info(f"Email verification token created: {context['token']}")

        subject = _("Verify your new email address")
        message = render_to_string(
            "users/email/profile_edit_email_verification_message.txt", context
        )

        # Proceed to send the verification email
        send_email_task.delay(subject, message, [user.email2])
        logger.info(f"Verification email sent to {user.username}")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = reverse("users:profile_edit_email")
        context["button_text"] = _("Save Changes")
        return context


def verify_email_change(request):
    token = request.GET.get("token")
    id = request.GET.get("id")

    try:
        pk = decode_base64_key(id)
        user = UserAuthManager.get_user_by_pk(pk)

        token_user = Tokenizer().decode(user.pk, user.email2, user.password,
                                        user.date_joined, token=token, max_age=settings.PASSWORD_RESET_TIMEOUT)

        user.email = user.email2
        user.email2 = ""
        user.save()

        messages.success(request, _("Your email address has been verified."))
        return redirect("users:profile")

    except User.DoesNotExist:
        messages.error(request, _("No user found with the provided token."))
        logger.error(f"No user found with the provided token")
        return redirect("users:profile")

    except SignatureExpired:
        messages.error(request, _("Your token has expired. Please try again."))
        logger.error(f"Expired email verification token")
        return redirect("users:profile")

    except BadSignature:
        # Handle the case for tampering or bad token
        logger.error(f"Invalid or tampered email verification token")
        messages.error(request, _("Invalid token. Please try again."))
        return redirect("users:profile")
