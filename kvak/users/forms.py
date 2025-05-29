from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from wagtail.users.forms import UserCreationForm, UserEditForm

from users.models import CustomUser


class CustomUserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("Email"),
    )
    country = CountryField().formfield(
        label=_("Nationality or country of residence"),
        widget=CountrySelectWidget(),
    )
    is_youth_worker = forms.BooleanField(
        required=False,
        label=_("Are you a young person or youth worker?"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self._meta.model.USERNAME_FIELD].widget.attrs["autofocus"] = False
        self.fields["first_name"].widget.attrs["autofocus"] = True

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "country",
            "is_youth_worker",
        )
        model = CustomUser


class CustomAdminUserEditForm(UserEditForm):
    country = CountryField().formfield(
        label=_("Nationality or country of residence"),
    )
    is_youth_worker = forms.BooleanField(
        required=False,
        label=_("Are you a young person or youth worker?"),
    )

    class Meta(UserEditForm.Meta):
        fields = UserEditForm.Meta.fields | {"country", "is_youth_worker"}


class CustomAdminUserCreationForm(UserCreationForm):
    country = CountryField().formfield(
        label=_("Nationality or country of residence"),
    )
    is_youth_worker = forms.BooleanField(
        required=False,
        label=_("Are you a young person or youth worker?"),
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields | {"country", "is_youth_worker"}
