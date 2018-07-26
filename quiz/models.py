from django.db import models

class Question(models.Model):
    label = models.CharField(max_length=100)

class Option(models.Model):
    label = models.CharField(max_length=100)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='options'
    )
    is_correct = models.BooleanField(default=False)
