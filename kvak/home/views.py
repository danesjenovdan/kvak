import json

from django.http import JsonResponse
from django.views.generic import View

from .models import (
    BaseMaterialPage,
    UserAnsweredQuestion,
    UserFinishedBaseMaterial,
    UserFinishedExcercisePage,
)


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

        # save answer
        answer_obj = UserAnsweredQuestion.objects.create(
            base_material_page_id=page_id,
            question_id=question_id,
            answer_data=answer,
            user=request.user,
        )

        # check if all questions are answered for this base material page
        page = BaseMaterialPage.objects.get(id=page_id)
        all_answered = True
        for question in page.questions:
            answered = UserAnsweredQuestion.objects.filter(
                user=request.user,
                base_material_page_id=page_id,
                question_id=question.id,
            ).exists()
            if not answered:
                all_answered = False
                break

        if not all_answered:
            return JsonResponse({"status": "success"})

        bm_finished_obj, created = UserFinishedBaseMaterial.objects.get_or_create(
            user=request.user,
            base_material=page,
        )

        # check if all base material pages are finished for this exercise
        exercise_page = page.get_parent().specific
        all_finished = True
        for bm_page in exercise_page.get_children().type(BaseMaterialPage).specific():
            finished = UserFinishedBaseMaterial.objects.filter(
                user=request.user,
                base_material=bm_page,
            ).exists()
            if not finished:
                all_finished = False
                break

        if not all_finished:
            return JsonResponse({"status": "success"})

        exercise_finished_obj, created = (
            UserFinishedExcercisePage.objects.get_or_create(
                user=request.user,
                exercise=exercise_page,
            )
        )

        return JsonResponse({"status": "success"})
