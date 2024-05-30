from users.forms import CustomUserCreationForm


class UsernameForm(CustomUserCreationForm):
    class Meta(CustomUserCreationForm.Meta):
        # Specify only the 'email' field to be used from the parent form
        fields = ["username"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = {
            'username': self.fields['username']
        }
