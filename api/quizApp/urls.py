from django.urls import path, include
from rest_framework import routers
from .views import QuizViewSet, QuestionViewSet, OptionViewSet


router = routers.DefaultRouter()
router.register('Quiz', QuizViewSet)
router.register('Question', QuestionViewSet)
router.register('Option', OptionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]