from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserEditForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "bio")
