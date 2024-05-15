from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models
from core.sessions.session_store import SessionStore
from django.conf import settings


class Session(AbstractBaseSession):
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    # error :   IntegrityError at /admin/
    #           null value in column "created_at" of relation "django_session_core" violates not-null constraint
    # the way django create session makes created_at not null
    # created_at = models.DateTimeField(auto_now_add=True, null=True)    
    updated_at = models.DateTimeField(auto_now=True)
    # urls_visited = models.TextField(blank=True, null=True)
    url_visited = models.URLField(blank=True, null=True, max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "django_session_core"

    @classmethod
    def get_session_store_class(cls):
        return SessionStore
