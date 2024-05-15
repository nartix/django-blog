from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string


class HTMXMixin():
    def get_fragment_template(self):
        return getattr(self, 'template_name', 'No fragment template set')

    def is_htmx_request(self):
        return self.request.headers.get("HX-Request", False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_htmx_request'] = self.is_htmx_request()
        return context

    def render_to_htmx(self, context, **response_kwargs):
        # Pre-render hook
        self.pre_render_hook(context)

        response = HttpResponse(render_to_string(
            self.get_fragment_template(), context, self.request), **response_kwargs)
        response['Vary'] = 'HX-Request'

        # Post-render hook
        self.post_render_hook(response)

        return response

    def pre_render_hook(self, context):
        pass

    def post_render_hook(self, response):
        pass

    def render_to_json(self, data, status=200):
        return JsonResponse(data, status=status)
