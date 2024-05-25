from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, View
from core.mixins import CoreMixin
from django.core.cache import cache
from core.tasks import send_email_task, hello_world
from core.tasks_kafka import my_first_kafka_task


class AboutView(CoreMixin, TemplateView):
    # template_name = "core/content.html"
    # fragment_template_name = "core/about.html"
    template_name = "core/about.html"
    title = _("About")


class IndexView(CoreMixin, TemplateView):
    template_name = "core/index.html"
    title = _("Home")


class ProjectsView(CoreMixin, TemplateView):
    template_name = "core/projects.html"
    title = _("Projects")


class Handler403View(CoreMixin, TemplateView):
    template_name = "core/errors/403.html"
    title = _("Error 403 - Forbidden")


class Handler404View(CoreMixin, TemplateView):
    template_name = "core/errors/404.html"
    title = _("Error 404 - Not Found")


class Handler401View(CoreMixin, TemplateView):
    template_name = "core/errors/401.html"
    title = _("Error 401 - Unauthorized")


def handler401(request):
    is_htmx_request = request.headers.get("HX-Request", False)
    context = {
        "title": _("Error 401 - Unauthorized"),
        "template": "core/errors/401.html",
        "is_htmx_request": is_htmx_request,
    }

    # send_email_task.delay(
    #     'Testing Celery',
    #     'Here is the message.',
    #     ['email@email.com']  # List of recipient email addresses
    # )

    # send_task_to_dynamic_broker('core.tasks.hello_world')
    # hello_world.delay()

    cache.set("my_key", "feroz cached", timeout=30)
    # my_first_kafka_task.__wrapped__(1, 2)
    # my_first_kafka_task(1, 2)

    print(cache.get("my_key"))

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)
