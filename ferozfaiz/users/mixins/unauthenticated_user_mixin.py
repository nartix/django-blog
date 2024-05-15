from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class UnauthenticatedUserMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('core:index')  # or your login view
