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
def has_options_with_image(question):
    options = question.value.get("answer_options", [])
    for option in options:
        if option.get("option_image"):
            return True
    return False


@register.simple_tag
def get_random_order(values, answered_question):
    # original order as fallback
    fallback = [
        {"original_index": i, "value": option} for i, option in enumerate(values)
    ]

    # if the question was not answered yet, return randomized options
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

    # if the question was already answered, we sort the options by the order in the answer
    answer_data = answered_question.answer_data

    if not isinstance(answer_data, list) or len(answer_data) == 0:
        return fallback

    if not all(isinstance(i, int) for i in answer_data):
        return fallback

    randomized = list()
    for ans_idx in range(len(answer_data)):
        i = answer_data[ans_idx]
        if i >= 0 and i < len(values):
            randomized.append({"original_index": i, "value": values[i]})

    return randomized


@register.simple_tag
def is_correct_order(priority_option, answered_question):
    if not answered_question:
        return False

    answer_data = answered_question.answer_data
    if not isinstance(answer_data, list):
        return False

    correct_order = priority_option.get("original_index")
    user_order = answer_data.index(correct_order)
    return correct_order == user_order


@register.simple_tag
def get_random_order_pair(values, answered_question):
    # original order as fallback
    fallback = {
        "left": [
            {"original_index": i, "value": option} for i, option in enumerate(values)
        ],
        "right": [
            {"original_index": i, "value": option} for i, option in enumerate(values)
        ],
    }

    # if the question was not answered yet, return randomized options
    if not answered_question:
        randomized = {"left": list(), "right": list()}

        original = list(values)
        original_len = len(original)

        original_indices = list(range(original_len))
        for i in range(original_len):
            choice_index = random.choice(original_indices)
            choice_value = original[choice_index]
            original_indices.remove(choice_index)
            randomized["left"].append(
                {"original_index": choice_index, "value": choice_value}
            )

        original_indices = list(range(original_len))
        for i in range(original_len):
            choice_index = random.choice(original_indices)
            choice_value = original[choice_index]
            original_indices.remove(choice_index)
            randomized["right"].append(
                {"original_index": choice_index, "value": choice_value}
            )

        return randomized

    # if the question was already answered, we sort the options by the order in the answer
    answer_data = answered_question.answer_data

    if (
        not isinstance(answer_data, dict)
        or "left" not in answer_data
        or "right" not in answer_data
        or "connections" not in answer_data
    ):
        return fallback

    answer_left = answer_data["left"]
    answer_right = answer_data["right"]
    answer_connections = answer_data["connections"]

    if (
        not isinstance(answer_left, list)
        or not isinstance(answer_right, list)
        or not isinstance(answer_connections, list)
    ):
        return fallback

    if (
        len(answer_left) != len(answer_right)
        or len(answer_left) != len(answer_connections)
        or not all(isinstance(i, int) for i in answer_left)
        or not all(isinstance(i, int) for i in answer_right)
        or not all(isinstance(i, list) and len(i) == 2 for i in answer_connections)
    ):
        return fallback

    print("Answer data:", answer_data)

    randomized = {"left": list(), "right": list()}
    for ans_idx in range(len(answer_left)):
        left_index = answer_left[ans_idx]
        right_index = answer_right[ans_idx]
        if (
            left_index >= 0
            and left_index < len(values)
            and right_index >= 0
            and right_index < len(values)
        ):
            randomized["left"].append(
                {"original_index": left_index, "value": values[left_index]}
            )
            randomized["right"].append(
                {"original_index": right_index, "value": values[right_index]}
            )

    return randomized


@register.simple_tag
def has_connection(list_name, answer_option, answered_question):
    if not answered_question:
        return None

    answer_data = answered_question.answer_data

    if (
        not isinstance(answer_data, dict)
        or "connections" not in answer_data
        or not isinstance(answer_data["connections"], list)
    ):
        return None

    connections = answer_data["connections"]

    if not all(isinstance(i, list) and len(i) == 2 for i in connections):
        return None

    for connection in connections:
        if list_name == "left":
            if connection[0] == answer_option.get("original_index"):
                return connection[1]
        elif list_name == "right":
            if connection[1] == answer_option.get("original_index"):
                return connection[0]

    return None
