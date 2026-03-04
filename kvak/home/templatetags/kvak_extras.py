import random

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
    if request.resolver_match:
        return request.resolver_match.url_name in AUTH_URL_NAMES
    return False


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


@register.simple_tag(takes_context=True)
def get_user_progress(context, course_page):
    user = context["request"].user
    if user.is_anonymous:
        return None
    return course_page.get_user_progress(user=user)


@register.filter
def randomize_with_original_index(values, answered_question):
    if not answered_question:
        original = list(values)
        original_len = len(original)
        original_indices = list(range(original_len))

        randomized = list()
        for i in range(original_len):
            choice_index = random.choice(original_indices)
            choice_value = original[choice_index]
            original_indices.remove(choice_index)
            randomized.append({"original_index": choice_index, "value": choice_value})

        return randomized
    else:
        # if the question was already answered, we sort the options by the order in
        # which they were answered
        answer_data = answered_question.answer_data

        if not isinstance(answer_data, list):
            # if the answer data is not a list, we can't sort the options, so we return
            # them in the original order
            return [
                {"original_index": i, "value": option}
                for i, option in enumerate(values)
            ]

        randomized = list()
        # for i in answer_data:
        for i in range(len(answer_data)):
            j = answer_data.index(i)
            if j >= 0 and j < len(values):
                randomized.append({"original_index": j, "value": values[j]})

        return randomized


@register.filter
def is_correct_order(priority_option, answered_question):
    if not answered_question:
        return False

    answer_data = answered_question.answer_data
    if not isinstance(answer_data, list):
        return False

    correct_order = priority_option.get("original_index")
    user_order = answer_data.index(correct_order)
    return correct_order == user_order
