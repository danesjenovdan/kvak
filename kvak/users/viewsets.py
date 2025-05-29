from wagtail.users.views.users import UserViewSet as WagtailUserViewSet

from users.forms import CustomAdminUserCreationForm, CustomAdminUserEditForm


class UserViewSet(WagtailUserViewSet):
    def get_form_class(self, for_update=False):
        if for_update:
            return CustomAdminUserEditForm
        return CustomAdminUserCreationForm
