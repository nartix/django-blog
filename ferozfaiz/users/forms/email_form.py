from users.forms import CustomUserCreationForm


class EmailForm(CustomUserCreationForm):
    class Meta(CustomUserCreationForm.Meta):
        # Specify only the 'email' field to be used from the parent form
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = {
            'email': self.fields['email']
        }
