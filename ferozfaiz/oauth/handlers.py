from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from urllib.parse import urlencode, urlunparse, urlparse
import uuid
import requests
import logging

logger = logging.getLogger('core')


class BaseOAuthHandler:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.validate_config()

    def validate_config(self):
        required_keys = ["client_id", "client_secret", "redirect_uri"]
        config = {"client_id": self.client_id,
                  "client_secret": self.client_secret, "redirect_uri": self.redirect_uri}
        if not all(key in config for key in required_keys):
            raise ValueError(
                f"{self.__class__.__name__} Missing required keys in configuration")

    def get_auth_params(self, state_id):
        raise NotImplementedError

    def get_auth_url(self, request):
        next = request.GET.get("next", "")

        if next:
            next_url = is_safe_url(next, allowed_hosts={request.get_host()})
            if next_url:
                state_id = str(uuid.uuid4())
                request.session[state_id] = {"next_url": next}
        else:
            state_id = ""

        params = self.get_auth_params(state_id)

        parsed_url = urlparse(self.AUTH_URL)
        auth_url = urlunparse(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', urlencode(params), ''))

        logger.info(f"{self.__class__.__name__} auth URL: {auth_url}")
        return auth_url

    def exchange_code(self, code):
        data = self.get_exchange_params(code)

        response = requests.post(self.TOKEN_URL, data=data)
        response.raise_for_status()  # Raises an exception for HTTP error codes

        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token", None)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def get_exchange_params(self, code):
        raise NotImplementedError

    def get_user_info(self, tokens):
        # Make a GET request to the user info endpoint
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        response = requests.get(self.USER_INFO_URL, headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP error codes
        user_info = response.json()

        # Process the user info
        processed_user_info = self.process_user_info(user_info, tokens)
        logger.info(
            f"{self.__class__.__name__} user received for {processed_user_info['uid']}")
        return processed_user_info


class GoogleOAuthHandler(BaseOAuthHandler):
    # Google's authorization server URLs
    AUTH_URL = settings.OAUTH_PROVIDERS["google"]["auth_url"]
    TOKEN_URL = settings.OAUTH_PROVIDERS["google"]["token_url"]
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def get_auth_params(self, state_id):
        SCOPES = ["https://www.googleapis.com/auth/userinfo.email",
                  "https://www.googleapis.com/auth/userinfo.profile"]
        return {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(SCOPES),
            "access_type": "offline",
            # "approval_prompt": "force",  # "force" to always show consent screen
            # "consent" to always show consent screen, needed if you need refresh token
            # "prompt": "consent",
            "state": state_id,
        }

    def get_exchange_params(self, code):
        return {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }

    def process_user_info(self, user_info, tokens):
        user_info["provider"] = "google"
        user_info["access_token"] = tokens["access_token"]
        user_info["refresh_token"] = tokens.get("refresh_token", None)
        user_info["uid"] = user_info["sub"]
        user_info["first_name"] = user_info.get("given_name") or ""
        user_info["last_name"] = user_info.get("family_name") or ""
        return user_info


class MicrosoftOAuthHandler(BaseOAuthHandler):
    AUTH_URL = settings.OAUTH_PROVIDERS["microsoft"]["auth_url"]
    TOKEN_URL = settings.OAUTH_PROVIDERS["microsoft"]["token_url"]
    USER_INFO_URL = settings.OAUTH_PROVIDERS["microsoft"]["user_info_url"]

    def get_auth_params(self, state_id):
        scope = "openid email profile User.Read offline_access"
        return {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "response_mode": "query",
            "state": state_id,
        }

    def get_exchange_params(self, code):
        return {
            "client_id": self.client_id,
            "scope": "openid email profile User.Read offline_access",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "client_secret": self.client_secret,
        }

    def process_user_info(self, user_info, tokens):
        user_info["provider"] = "microsoft"
        user_info["access_token"] = tokens["access_token"]
        user_info["refresh_token"] = tokens.get("refresh_token", None)
        user_info["uid"] = user_info["id"] or user_info.get("sub")
        user_info["first_name"] = user_info.get("givenName") or ""
        user_info["last_name"] = user_info.get("surname") or ""
        user_info["email"] = user_info.get(
            "userPrincipalName") or user_info.get("mail")
        if not user_info["email"]:
            logger.error("No email address available in user info.")
            return None
        return user_info


HANDLERS = {
    "google": GoogleOAuthHandler,
    "microsoft": MicrosoftOAuthHandler,
}


def get_oauth_handler(provider_name):
    oauth_settings = settings.OAUTH_PROVIDERS.get(provider_name)

    if not oauth_settings:
        raise ValueError("Unsupported provider")

    handler_class = HANDLERS.get(provider_name)

    if not handler_class:
        raise ValueError("Unsupported provider")

    return handler_class(
        oauth_settings["client_id"],
        oauth_settings["client_secret"],
        oauth_settings["redirect_uri"],
    )


def get_oauth_url(provider_name, request):
    handler = get_oauth_handler(provider_name)
    return handler.get_auth_url(request)
