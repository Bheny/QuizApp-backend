from rest_framework import serializers
from .models import Quiz, Question, Option, Classroom



class ClassroomSerializer(serializers.ModelSerializer):
    quizes = serializers.SerializerMethodField()
    class Meta:
        model = Classroom
        fields = ['id','name','lecturer','quizes']

    def get_quizes(self, obj):
        quizes = obj.get_all_quizes()
        serializer = QuizSerializer(quizes, many=True)
        return serializer.data

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'text', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'text', 'options')

    def get_options(self, obj):
        options = obj.get_all_options()
        serializer = OptionSerializer(options, many=True)
        return serializer.data

class QuizSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description','questions']
        
    def get_questions(self, obj):
        questions = obj.get_all_questions()
        serializer = QuestionSerializer(questions, many=True)
        return serializer.data
