# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from wagtail.users.forms import UserCreationForm, UserEditForm

from users.models import CustomUser


class CustomUserForm(DjangoUserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("Email Address"),
        help_text=_("Enter a valid email address."),
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    country = CountryField()
    is_youth_worker = forms.BooleanField(
        required=False,
        label=_("Is Youth Worker"),
        help_text=_("Check this box if user is a youth worker."),
    )

    class Meta:
        fields = ("email", "country", "is_youth_worker")
        widgets = {
            "country": forms.Select(attrs={"class": "form-control"}),
            "is_youth_worker": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        model = CustomUser


class CustomUserEditForm(UserEditForm):
    country = CountryField()
    is_youth_worker = forms.BooleanField(
        required=False,
        label=_("Is Youth Worker"),
        help_text=_("Check this box if user is a youth worker."),
    )

    class Meta(UserEditForm.Meta):
        fields = UserEditForm.Meta.fields | {"country", "is_youth_worker"}


class CustomUserCreationForm(UserCreationForm):
    country = CountryField()
    is_youth_worker = forms.BooleanField(
        required=False,
        label=_("Is Youth Worker"),
        help_text=_("Check this box if user is a youth worker."),
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields | {"country", "is_youth_worker"}
