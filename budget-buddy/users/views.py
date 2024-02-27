"""Accounts view."""
from django.urls import reverse_lazy
from django.views import generic

from users.forms import CustomUserCreationForm
from users.models import CustomUser


class SignUpView(generic.CreateView):
    """Sign up view for Users."""

    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "generic_create_update_form.html"
    success_url = reverse_lazy("login")
    extra_context = {"title_text": "Sign Up", "button_text": "Register"}
