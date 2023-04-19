from django import forms
from .models import Quiz, Answer, Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'questions_count']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['label', 'order']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
