from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

# Create your views here.


def index(request):
    is_htmx_request = request.headers.get("HX-Request", False)
    context = {"title": _("Home"), "template": "core/index.html",
               "is_htmx_request": is_htmx_request}

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)


def projects(request):
    is_htmx_request = request.headers.get("HX-Request", False)
    context = {"title": _("Projects"),
               "template": "core/projects.html", "is_htmx_request": is_htmx_request}

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)


def about(request):
    is_htmx_request = request.headers.get("HX-Request", False)
    context = {"title": _("About"), "template": "core/about.html",
               "is_htmx_request": is_htmx_request}

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)


# def handler403(request, exception):
def handler403(request):
    is_htmx_request = request.headers.get("HX-Request", False)
    context = {"title": _("Error 403 - Forbidden"),
               "template": "core/errors/403.html", "is_htmx_request": is_htmx_request}

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)


# def handler404(request, exception):
def handler404(request):
    is_htmx_request = request.headers.get("HX-Request", False)
    context = {"title": _("Error 404 - Not Found"),
               "template": "core/errors/404.html", "is_htmx_request": is_htmx_request}

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)


def handler401(request):
    is_htmx_request = request.headers.get("HX-Request", False)
    context = {"title": _("Error 401 - Unauthorized"),
               "template": "core/errors/401.html", "is_htmx_request": is_htmx_request}

    if is_htmx_request:
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)
