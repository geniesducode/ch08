from django.shortcuts import render, get_object_or_404, redirect
from quiz.models import Question
from quiz.utils import get_rank

def home(request):
    question = Question.objects.first()
    return render(request, 'quiz/home.html', {'question': question})

def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        if 'answers' not in request.session:
            request.session['answers'] = {}

        request.session['answers'][str(question.id)] = (
            request.POST.get('option')
        )
        request.session.modified = True
        next_question = question.get_next_question()

        if next_question:
            return redirect('question_detail', question_id=next_question.id)
        else:
            return redirect('results')

    context = {
        'question': question,
        'options': question.options.all(),
        'nb_questions': Question.objects.count(),
        'question_number': question.get_number(),
    }
    return render(request, 'quiz/question_detail.html', context)

def results(request):
    total_questions = Question.objects.count()
    answered_questions = len(request.session.get('answers', {}))

    if answered_questions != total_questions:
        return redirect('home')

    score = 0
    for question in Question.objects.all():
        answer = request.session['answers'][str(question.id)]
        if question.is_correct(answer):
            score += 1

    score_percentage = int(score / total_questions * 100)
    rank = get_rank(score_percentage)
    del request.session['answers']

    return render(request, 'quiz/results.html', {
        'score': score_percentage,
        'title': rank['title'],
        'description': rank['description']
    })
