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
]


@register.filter
def is_login_page(request):
    return request.resolver_match.url_name in AUTH_URL_NAMES
