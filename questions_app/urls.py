from django.urls import path
from .views import QuizesListView, QuizCreateView, QuizView

urlpatterns = [
    path('', QuizesListView.as_view(), name = "home_page"),
    path('<str:quiz>/', QuizView.as_view(), name="quiz_questions"),
    path('createquiz/new/', QuizCreateView.as_view(), name = "create_quiz"),
]