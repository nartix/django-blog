from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import bleach
from blogs.models import BlogPost


class BlogPostForm(forms.ModelForm):
    content = forms.CharField(max_length=3000, widget=forms.Textarea)

    class Meta:
        model = BlogPost
        fields = ['title', 'content']

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        self.stripped_content = bleach.clean(
            content, tags=[], strip=True).strip()
        if not self.stripped_content:
            raise ValidationError(_("Content cannot be empty."))
        return content
