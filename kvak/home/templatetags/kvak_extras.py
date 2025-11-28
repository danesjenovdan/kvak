from django import template

from home.models import UserAnsweredQuestion

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


@register.simple_tag(takes_context=True)
def get_user_answered_question(context, base_material_page, question):
    user = context["request"].user
    if user.is_anonymous:
        return None
    return (
        UserAnsweredQuestion.objects.filter(
            user=user,
            base_material_page_id=base_material_page.id,
            question_id=question.id,
        )
        .order_by("-answered_at")
        .first()
    )
