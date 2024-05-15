from users.forms import CustomUserCreationForm


class UsernameForm(CustomUserCreationForm):
    class Meta(CustomUserCreationForm.Meta):
        fields = [
            "username"
        ]  # Specify only the 'email' field to be used from the parent form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove fields not required for this form
        del self.fields["email"]
        del self.fields["password1"]
        del self.fields["password2"]
