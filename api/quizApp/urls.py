from django.urls import path, include
from rest_framework import routers
from .views import QuizViewSet, QuestionViewSet, OptionViewSet, ClassroomViewSet


router = routers.SimpleRouter()
router.register('Classroom', ClassroomViewSet)
router.register('Quiz', QuizViewSet)
router.register('Question', QuestionViewSet)
router.register('Option', OptionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('quizzes/<int:pk>/upload-questions/', QuizViewSet.as_view({'post': 'upload_questions'})),
    path('Classroom/get_classrooms_by_name/<str:Name>/', ClassroomViewSet.as_view({'get':'get_classroom_by_Name'})), 
]