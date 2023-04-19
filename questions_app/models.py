from django.db import models
import uuid
# Create your models here.

class Quiz(models.Model):
    name = models.CharField(max_length=1000)
    questions_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add= True, null= True, blank=True)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    label = models.CharField(max_length=1000)
    order = models.IntegerField(default=0)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    is_correct = models.BooleanField(default=False)

