from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status 
import openpyxl
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    action(detail=True, methods=['post'])
    def upload_answers(self, request, pk):
        # Get the quiz object with the given ID
        quiz = get_object_or_404(Quiz, id=pk)
        
        # Parse the user's answers from the request body
        submitted_answers = request.data['answers']
        
        # Validate the user's answers
        if not submitted_answers:
            return Response({'error': 'No answers submitted'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the user's answers to the database
        for answer in submitted_answers:
            student_id = answer['student_id']
            question_id = answer['question_id']
            selected_option_id = answer['selected_option_id']
            question = get_object_or_404(Question, id=question_id, quiz=quiz)
            selected_option = get_object_or_404(Option, id=selected_option_id, question=question)
            Submission.objects.create(user=Student.object.get(id=student_id), quiz=quiz, question=question, selected_option=selected_option)
        
        # Return a success message
        return Response({'message': 'Answers submitted successfully'}, status=status.HTTP_201_CREATED)


class ClassroomViewSet(viewsets.ModelViewSet):
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()

    @action(detail=False, methods=['get'])
    def get_classroom_by_Name(self, request, Name=None):
        try:
            classroom = Classroom.objects.get(name=Name)
            serializer = ClassroomSerializer(classroom)
            return Response(serializer.data)
        except Classroom.DoesNotExist:
            return Response({'error':'This Classroom does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            # raise Http404


class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer 
    queryset = Quiz.objects.all()
    
    @action(detail=True, methods=['post'])
    def upload_questions(self, request, pk=None):
        quiz = self.get_object()

        # Check if a file was uploaded
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Please provide a file to upload.'}, status=status.HTTP_400_BAD_REQUEST)

        # Load the Excel file
        try:
            workbook = openpyxl.load_workbook(file)
            worksheet = workbook.active
        except Exception as e:
            return Response({'error': f'Failed to load the file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the questions and answers from the Excel file
        questions = []
        for row in worksheet.iter_rows(min_row=2):
            text = row[0].value
            answers = []
            for cell in row[1:]:
                if cell.value:
                    answers.append(cell.value)
            questions.append({'text': text, 'answers': answers})
            print(questions)

        # Create the questions and answers
        for question_data in questions:
            question = Question.objects.create(text=question_data['text'], quiz=quiz)
            for answer_text in question_data['answers']:
                is_correct = answer_text.startswith('*')
                answer_text = answer_text.lstrip('*')
                Option.objects.create(text=answer_text, is_correct=is_correct, question=question)

        return Response({'success': f'Successfully uploaded {len(questions)} questions to the quiz.'})

class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

class OptionViewSet(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    queryset = Assessment.objects.all()


    def update(self, request, pk=None):
        pass
