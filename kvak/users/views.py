from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomUserForm


class SignUpView(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
