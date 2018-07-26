from django.db import models

class Question(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Option(models.Model):
    label = models.CharField(max_length=100)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='options'
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.label
