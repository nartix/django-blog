from django.utils.translation import gettext as _
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.cache import cache
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
import bleach
import logging
from core.mixins import CoreMixin
from blogs.models import BlogPost
from blogs.forms import BlogPostForm
from core.pagination import CachingPaginator
from core.utils import sanitize_html

logger = logging.getLogger('core')


class BlogDetailView(CoreMixin, TemplateView):
    template_name = "blogs/blog_list_copy.html"
    title = _("Blog List")


class BlogListView(CoreMixin, ListView):
    model = BlogPost
    template_name = "blogs/blog_list.html"
    title = _("Blog List")
    paginate_by = 3
    context_object_name = "blogs"
    queryset = BlogPost.objects.select_related(
        'author').filter(status=1)
    ordering = "-updated_at"
    extra_context = {
        "title": title,
        "description": "This is a blog list page",
        "keywords": "blog, list, page",
        "paginate_range": 2,
    }

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        cache_key = f"blog_list_count"
        cache_timeout = 30
        return CachingPaginator(queryset, per_page, cache_key, cache_timeout, orphans=orphans, allow_empty_first_page=allow_empty_first_page, **kwargs)

    # cache the whole queryset
    # def get_queryset(self):
    #     queryset = cache.get('blog_list')

    #     if not queryset:
    #         queryset = BlogPost.objects.select_related(
    #             'author').filter(status=1).order_by(self.ordering)
    #         cache.set('blog_list', queryset, 30)  # Cache for 30 seconds

    #     return queryset


class BlogPostDetailView(CoreMixin, DetailView):
    model = BlogPost
    template_name = "blogs/blog_detail.html"
    context_object_name = "blog"
    title = _("Blog Detail")
    queryset = BlogPost.objects.select_related('author').filter(status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        # context["description"] = "This is a blog detail page"
        # context["keywords"] = "blog, detail, page"
        return context


class BlogPostCreateView(LoginRequiredMixin, CoreMixin, CreateView):
    model = BlogPost
    template_name = "blogs/blog_form.html"
    title = _("Create Blog Post")
    success_url = reverse_lazy('blogs:blog_list')
    form_class = BlogPostForm

    def form_valid(self, form):
        form.instance.content = sanitize_html(form.cleaned_data['content'])
        form.instance.author = self.request.user
        form.instance.status = 1
        return super().form_valid(form)

    def form_invalid(self, form):
        if 'content' in form.cleaned_data:
            sanitized_content = sanitize_html(form.cleaned_data['content'])
            # Update the form's content field to the sanitized version for safety in re-display
            form.data = form.data.copy()  # Make the QueryDict mutable
            form.data['content'] = sanitized_content

        return super().form_invalid(form)


class BlogPostUpdateView(LoginRequiredMixin, CoreMixin, UpdateView):
    model = BlogPost
    template_name = "blogs/blog_form.html"
    title = _("Update Blog Post")
    # success_url = reverse_lazy("blogs:blog_detail")
    form_class = BlogPostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["button_text"] = _("Update Post")
        context["blog"] = self.blog
        return context

    def dispatch(self, request, *args, **kwargs):
        self.blog = self.get_object()
        if self.blog.author != request.user and not request.user.is_superuser:
            return redirect('blogs:blog_list')
        return super(BlogPostUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blogs:blog_detail', args=[self.object.id, self.object.slug])


class BlogPostDeleteView(LoginRequiredMixin, CoreMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blogs:blog_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user and not request.user.is_superuser:
            return redirect(self.success_url)
        response = super(BlogPostDeleteView, self).dispatch(
            request, *args, **kwargs)
        messages.success(request, 'Blog post was deleted successfully.')
        return response
