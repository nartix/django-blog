from django.urls import path
from .views import (
    login,
    callback,
    OAuthSignupUsernameView,
    login_link_token,
)

app_name = "oauth"

urlpatterns = [
    path("accounts/login/<str:provider_name>/", login, name="oauth_login"),
    path("accounts/login/<str:provider_name>/callback/", callback, name="callback"),
    path(
        "accounts/signup/username/",
        OAuthSignupUsernameView.as_view(),
        name="signup_username",
    ),
    path(
        "accounts/link/<str:provider_name>/<token>/",
        login_link_token,
        name="login_link_token",
    ),
]
