import json

from django.http import JsonResponse
from django.views.generic import View

from .models import BaseMaterialPage, UserAnsweredQuestion


class AnswerView(View):
    def post(self, request, *args, **kwargs):
        if not request.user or request.user.is_anonymous:
            return JsonResponse(
                {"status": "error", "message": "Authentication required"}, status=401
            )

        data = json.loads(request.body)

        page_id = data.get("page_id", None)
        question_id = data.get("question_id", None)
        answer = data.get("answer", None)

        if not page_id or not question_id or answer is None:
            return JsonResponse(
                {"status": "error", "message": "Invalid data"}, status=400
            )

        page_exists = BaseMaterialPage.objects.filter(id=page_id).exists()
        if not page_exists:
            return JsonResponse(
                {"status": "error", "message": "Page does not exist"}, status=404
            )

        obj = UserAnsweredQuestion.objects.create(
            base_material_page_id=page_id,
            question_id=question_id,
            answer_data=answer,
            user=request.user,
        )

        return JsonResponse({"status": "success"})
