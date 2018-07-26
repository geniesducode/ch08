from django.shortcuts import render, get_object_or_404
from quiz.models import Question

def home(request):
    return render(request, 'quiz/home.html')

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    context = {
        'question': question,
        'options': question.options.all(),
        'nb_questions': Question.objects.count(),
        'question_number': question.get_number(),
    }
    return render(request, 'quiz/question_detail.html', context)
