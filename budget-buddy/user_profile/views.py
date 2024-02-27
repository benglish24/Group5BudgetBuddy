"""User profile view."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from . import forms, mixins, models


# Create your views here.
class UserProfileDetailView(mixins.UserProfileRequiredMixin, generic.DetailView):
    """Profile detail view."""

    model = models.UserProfile
    template_name = "user_profile/userprofile_detail.html"
    slug_field = None
    slug_url_kwarg = ""

    def get_object(self, queryset=None):
        """Owner of the object should be the current user."""
        return self.model.objects.filter(custom_user=self.request.user).first()


class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Profile update view."""

    model = models.UserProfile
    form_class = forms.UserProfileUpdateForm
    success_url = reverse_lazy("user_profile:profile_detail")
    template_name = "generic_create_update_form.html"
    extra_context = {"title_text": "Update Profile", "button_text": "Update"}

    def get_object(self, queryset=None):
        """Get the `UserProfile` object the current logged in user."""
        return self.model.objects.filter(custom_user=self.request.user).first()

    def get_context_data(self, **kwargs):
        """Add additional fields to the form."""
        context = super().get_context_data(**kwargs)

        user_profile = self.request.user.userprofile

        initial = {
            "first_name": self.request.user.first_name,
            "last_name": self.request.user.last_name,
        }

        context["form"] = forms.UserProfileUpdateForm(instance=user_profile, initial=initial)

        return context

    def form_valid(self, form):
        """Set custom_user Field of the current object as the current user."""
        user_profile = form.save(commit=False)
        user_profile.custom_user = self.request.user

        custom_user = self.request.user
        custom_user.first_name = form.cleaned_data["first_name"]
        custom_user.last_name = form.cleaned_data["last_name"]
        user_profile.save()
        custom_user.save()

        return super().form_valid(form)
