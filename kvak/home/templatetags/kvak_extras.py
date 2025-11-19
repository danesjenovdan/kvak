from django import template

register = template.Library()


AUTH_URL_NAMES = [
    "login",
    "logout",
    "password_change",
    "password_change_done",
    "password_reset",
    "password_reset_done",
    "password_reset_confirm",
    "password_reset_complete",
    "register",
    "profile",
]


@register.filter
def is_profile_page(request):
    return request.resolver_match.url_name in AUTH_URL_NAMES


@register.filter
def debug_print(value):
    print("-----")
    print(type(value))
    print(value)
    print(dir(value))
    print(vars(value))
    print("-----")
    return ""
