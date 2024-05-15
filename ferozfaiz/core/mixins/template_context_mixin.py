# create a mixin to input some common template context data
from django.views.generic.base import ContextMixin
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.conf import settings


class TemplateContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        context["template"] = self.get_template_name()
        context["next"] = self.get_next_url()
        context["APPDATA"] = settings.APPDATA
        return context

    def get_next_url(self):
        self.next = self.request.GET.get("next", "")
        url_validator = URLValidator()
        try:
            url_validator(self.next)
        except ValidationError:
            return ""
        return (
            self.next
            if is_safe_url(self.next, allowed_hosts={self.request.get_host()})
            else ""
        )

    def get_title(self):
        return getattr(self, "title", "No title set")

    def get_template_name(self):
        return getattr(self, "template_name", "No fragment template set")

    def get_fragment_template(self):
        return getattr(self, "fragment_template_name", "No fragment template set")
