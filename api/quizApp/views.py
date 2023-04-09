from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status 
import openpyxl
# Create your views here.

class ClassroomViewSet(viewsets.ModelViewSet):
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()

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








