from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Quiz, Question, Answer
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer
import json
from django.http import JsonResponse, HttpResponse
from . import quiz_form
from urllib.parse import unquote
# Create your views here.


class QuizesListView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class= QuizSerializer
    lookup_field = 'name'
    
    
    def get(self, request, *args, **kwargs):
        print("Headers")
        user_agent = request.headers.get('User-Agent')
        mobile_app = request.headers.get('mobile_app')
        print(user_agent)
        print(mobile_app)
        queryset = self.get_queryset()
        serializer = QuizSerializer(queryset, many = True)
        return render(request, 'all_quizes_template.html', {'data': serializer.data, 'mobile_app' : mobile_app})
    
    def delete(self, request, *args, **kwargs):
        data = request.data
        name = data['quiz']
        quiz = Quiz.objects.get(name = name)
        quiz.delete()
        return JsonResponse( {'response_data': 'Sucess'},status = 200 )

 
class QuizView(generics.ListCreateAPIView):
    
    def get(self,request, *args, **kwargs):
        quiz_name =  unquote(kwargs['quiz'])
        question_queryset = Question.objects.filter(quiz__name = quiz_name)
        question_serializer = QuestionSerializer(instance = question_queryset, many= True)

        question_answers = {}
        
        for quest in question_serializer.data:
            print(quest)
            quest = json.dumps(quest)
            new_quest = json.loads(quest)
            answer_queryset = Answer.objects.filter(question__label = new_quest['label'])
            answer_serializer = AnswerSerializer(instance = answer_queryset, many= True).data
            answer_serializer_1 = json.dumps(answer_serializer)
            new_answer_serializer = json.loads(answer_serializer_1)
            question_answers[new_quest['label']] = new_answer_serializer

        return render(request, 'quiz_template.html', {'questions' : question_answers, 'questions_str': json.dumps(question_answers), 'quiz_name':quiz_name})
    
    
    def post(self,request, *args, **kwargs):
        data = request.data
        result_data_obj = {}
        correct_ans_count = 0
        for question, answer in data.items():
            correct_answer_obj = Answer.objects.filter(question__label = question, is_correct = True);
            correct_answer_ser = AnswerSerializer(instance = correct_answer_obj, many = True).data
            correct_answer_ser_1 = json.dumps(correct_answer_ser)
            correct_answer_ser_2 = json.loads(correct_answer_ser_1)
            correct_answer = correct_answer_ser_2[0]['text']

            if correct_answer == answer:
                correct_ans_count += 1

        result_data_obj['correct_ans'] = str(correct_ans_count)
        result_data = json.dumps(result_data_obj)

        return JsonResponse({'result_data' : result_data}, status = 200 )

class QuizCreateView(generics.ListCreateAPIView):
    
    def get(self,request, *args, **kwargs):
        quiz_name_form = quiz_form.QuizForm()
        question_forms = [quiz_form.QuestionForm(prefix=f'question_{i}') for i in range(3)]
        answer_forms = [[quiz_form.AnswerForm(prefix=f'question_{i}_answer_{j}') for j in range(3)] for i in range(3)]
        context = {
            'quiz_form': quiz_name_form,
            'question_forms': zip(question_forms, answer_forms),
        }
        return render(request, 'create_new_quiz.html', context)
    
    def post(self,request, *args, **kwargs):
        data = request.data
        for quiz_name, questions in data.items():
            quiz_data = {'name': quiz_name, 'questions_count': str(len(questions))}
            quiz_serializer = QuizSerializer(data = quiz_data)
            if quiz_serializer.is_valid():
                quiz = quiz_serializer.save()
            order_no = 1
            for question, answers in questions.items():
                question_data = {'quiz': quiz.id, 'label': question, 'order': order_no}
                print(question_data)
                order_no = order_no + 1
                question_serializer = QuestionSerializer(data = question_data)
                if question_serializer.is_valid():
                    question = question_serializer.save()

                answers_1 =  json.dumps(answers)
                answers_dict = json.loads(answers_1)

                for i in answers_dict['options']:
                    answer_data = {'question' : question.id, 'text': i, 'is_correct':False }
                    if i == answers_dict['correct_answer']:
                        answer_data = {'question' : question.id, 'text': i, 'is_correct':True }
                    answer_serializer = AnswerSerializer(data = answer_data)
                    if answer_serializer.is_valid():
                        answer = answer_serializer.save()

        return JsonResponse( {'response_data': 'Sucess'},status = 200 )


