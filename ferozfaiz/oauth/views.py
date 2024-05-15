from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, get_user_model
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.utils.translation import gettext as _
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
import logging

from users.forms import UsernameForm
from core.mixins import CoreMixin
from core.utils import redirect_with_message
from oauth.models import OAuthProvider
from oauth.handlers import get_oauth_handler, get_oauth_url
from oauth.utils import authenticate_oauth
from users.utils import get_user_id_from_token, UserAuthManager

logger = logging.getLogger("core")

User = get_user_model()


@login_required
def login_link_token(request, provider_name, token):
    try:
        # Verify the token and get the user's id, the token is valid for 5 hours 5 * 60 * 60
        uid = get_user_id_from_token(token, 5 * 60 * 60)
    except Exception as e:
        logger.error(f"Error during token verification: {e}")
        return redirect_with_message(
            request,
            "error",
            "There was an error processing your request. Please try again.",
            "users:profile",
        )

    if uid != request.user.pk:
        return redirect_with_message(
            request,
            "error",
            "Unable to link accounts. Please try again.",
            "users:profile",
        )

    return HttpResponseRedirect(get_oauth_url(provider_name, request))


def login(request, provider_name):
    if not OAuthProvider.objects.filter(Q(name=provider_name)).exists():
        return redirect_with_message(
            request,
            "error",
            "Unsupported provider.",
            "users:login",
        )

    if request.user.is_authenticated:
        return redirect("users:profile")

    return HttpResponseRedirect(get_oauth_url(provider_name, request))


# def handle_user_authentication(request, provider_name, user_info, next_url):
#     email = user_info.get("email")
#     if not email:
#         logger.error("OAuth callback did not return an email")
#         return redirect_with_message(
#             request,
#             "error",
#             "We were unable to retrieve your email address. Please provide it manually.",
#             "users:login",
#         )
#     try:
#         # Check if the email is associated with an existing OAuthUser
#         oauth_user = UserAuthManager.get_oauth_user(email, provider_name)
#         logger.info(
#             f"OAuthUser found: {oauth_user.user.username if oauth_user else None}")

#         if oauth_user:
#             # Existing OAuthUser found, check if the user is already logged in
#             if request.user.is_authenticated and request.user != oauth_user.user:
#                 # Logged in but the accounts do not match, prevent linking
#                 return redirect_with_message(
#                     request,
#                     "error",
#                     "This OAuth account is already linked to another user account.",
#                     "users:profile",
#                 )
#             else:
#                 # Login and update the OAuthUser with the latest info
#                 UserAuthManager.create_or_update_oauth_user(
#                     oauth_user.user, user_info)
#                 auth_login(request, oauth_user.user)

#                 if next_url:
#                     return redirect(next_url)

#                 return redirect("core:index")
#         else:
#             if request.user.is_authenticated:
#                 # User is logged in, link the account if not linked to another OAuth account
#                 UserAuthManager.create_or_update_oauth_user(
#                     request.user, user_info)
#                 return redirect_with_message(
#                     request,
#                     "success",
#                     "Your account has been linked successfully.",
#                     "users:profile",
#                 )
#             else:
#                 # No OAuthUser found, attempt to find or create a new user
#                 try:
#                     user = UserAuthManager.get_user_by_email(email)
#                     # Existing user found, ask to link accounts manually
#                     return redirect_with_message(
#                         request,
#                         "error",
#                         "An account with your email already exists. Please log in and link your accounts manually.",
#                         "users:login",
#                     )
#                 except User.DoesNotExist:
#                     # No User found, save the OAuth user info in the session for further processing in the signup flow
#                     request.session["oauth_user_info"] = user_info

#                     if next_url:
#                         request.session["next_url_after_oauth_signup"] = next_url

#                     # Redirect to a special OAuth signup page to complete their profile
#                     return redirect("oauth:signup_username")
#     except User.DoesNotExist:
#         request.session["oauth_user_info"] = user_info
#         if next_url:
#             request.session["next_url_after_oauth_signup"] = next_url
#         return redirect("oauth:signup_username")
#     except Exception as e:
#         logger.error(f"Error during oauth user authentication process: {e}")
#         return redirect_with_message(request, 'error', "There was an error processing your request. Please try again.", "users:login")


def callback(request, provider_name):
    code = request.GET.get("code")
    state_id = request.GET.get("state")
    state_data = request.session.pop(state_id, None)
    next_url = state_data.get('next_url') if state_data else None

    if "error" in request.GET:
        return redirect_with_message(
            request,
            "error",
            "Access was denied or a similar error occurred. Please try again.",
            "users:login",
        )

    try:
        handler = get_oauth_handler(provider_name)
        tokens = handler.exchange_code(code)
        user_info = handler.get_user_info(tokens)
    except Exception as e:
        logger.error(f"Error during OAuth callback: {e}")
        return redirect_with_message(
            request,
            "error",
            "There was an error processing your request. Please try again.",
            "users:login",
        )

    return authenticate_oauth(request, provider_name, user_info, next_url)


class OAuthSignupUsernameView(CoreMixin, FormView):
    template_name = "core/form/form_minimum.html"
    success_url = reverse_lazy("core:index")
    title = _("Almost Done")
    form_class = UsernameForm

    def form_valid(self, form):
        oauth_user_info = self.request.session.get("oauth_user_info")

        if oauth_user_info:
            self.user = UserAuthManager.create_user_and_oauth_accounts(
                form.cleaned_data, oauth_user_info)

            # Assuming user is correctly set in create_user_and_oauth_profile method
            auth_login(self.request, self.user)

            del self.request.session["oauth_user_info"]

            logger.info(
                f"User {self.user.username} signed up via OAuth with {oauth_user_info['provider']}"
            )

        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.session.pop(
            'next_url_after_oauth_signup', None)
        if next_url and is_safe_url(url=next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        else:
            return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = reverse("oauth:signup_username")
        context["form_message"] = _("Finish by choosing your username")
        context["button_text"] = _("Finish my account setup")
        return context
