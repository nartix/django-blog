from core.mixins import HTMXMixin, TemplateContextMixin

import logging

logger = logging.getLogger("core")


class CoreMixin(HTMXMixin, TemplateContextMixin):
    content_template_name = "core/content.html"

    def get_content_template_name(self):
        return self.content_template_name

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return`
        a list. May not be called if render_to_response is overridden.
        """
        return [self.get_content_template_name()]

    def render_to_response(self, context, **response_kwargs):
        """
        Renders the response, automatically handling HTMX requests by rendering
        the fragment if applicable, or falling back to the default rendering logic.
        """
        if self.is_htmx_request():
            logger.info("HTMX request detected")
            return self.render_to_htmx(context)
        else:
            if hasattr(super(), "render_to_response"):
                logger.info(
                    "Non-HTMX request detected and (super) render_to_response() called"
                )
                return super().render_to_response(context, **response_kwargs)
            else:
                logger.info(
                    "Non-HTMX request detected and manually rendering content.html"
                )
                # For the generic View, we manually render using the standard template
                from django.shortcuts import render

                return render(self.request, self.get_content_template_name(), context)
