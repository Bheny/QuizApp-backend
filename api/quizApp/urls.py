from django.urls import path, include
from rest_framework import routers
from .views import QuizViewSet, QuestionViewSet, OptionViewSet, ClassroomViewSet


router = routers.DefaultRouter()
router.register('Classroom', ClassroomViewSet)
router.register('Quiz', QuizViewSet)
router.register('Question', QuestionViewSet)
router.register('Option', OptionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('quizzes/<int:pk>/upload-questions/', QuizViewSet.as_view({'post': 'upload_questions'})),
]