from django.urls import path, include
from rest_framework import routers
from .views import QuizViewSet, QuestionViewSet, OptionViewSet, ClassroomViewSet, SubmissionViewSet,StudentViewSet, AssessmentViewSet


router = routers.SimpleRouter()
router.register('Classroom', ClassroomViewSet)
router.register('Quiz', QuizViewSet)
router.register('Question', QuestionViewSet)
router.register('Option', OptionViewSet)
router.register('Student', StudentViewSet)
router.register('Submissions', SubmissionViewSet)
router.register('Assessment', AssessmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('quizzes/<int:pk>/upload-questions/', QuizViewSet.as_view({'post': 'upload_questions'})),
    path('quizzes/<int:pk>/upload_answers/',QuizViewSet.as_view({'post':'upload_answers'})),
    path('Classroom/get_classrooms_by_name/<str:Name>/', ClassroomViewSet.as_view({'get':'get_classroom_by_Name'})), 
]