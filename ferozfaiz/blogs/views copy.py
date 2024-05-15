from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.translation import gettext as _


def blog_list(request):
    is_htmx_request = request.headers.get('HX-Request', False)
    context = {"title": _("Blogs"), "template": "blogs/blog_list.html",
               "is_htmx_request": is_htmx_request}

    if request.headers.get('HX-Request', False):
        fragment = render_to_string(context["template"], context, request)
        return HttpResponse(fragment)

    return render(request, "core/content.html", context)
