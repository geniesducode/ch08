from django.shortcuts import render, get_object_or_404, redirect
from quiz.forms import NameForm
from quiz.models import Question, Result
from quiz.utils import get_rank

def home(request):
    # L'utilisation d'un formulaire Django permet de le laisser s'occuper de la validation et du code HTML du
    # formulaire. Plus d'infos sur https://geniesducode.com/formulaires-django
    name_form = NameForm()

    if request.method == 'POST':
        name_form = NameForm(request.POST)

        # Si la personne laisse le champ "nom" vide, le formulaire ne sera pas valide: il faut alors réafficher la page
        # avec le formulaire et ses erreurs
        if name_form.is_valid():
            # Le nom est stocké dans la session pour être réutilisé plus tard
            request.session['name'] = name_form.cleaned_data['name']
            question = Question.objects.first()

            return redirect('question_detail', question_id=question.id)

    return render(request, 'quiz/home.html', {'form': name_form})

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

    # Enregistre le résultat dans la base de données en reprenant le nom donné au début du quiz
    Result.objects.create(name=request.session['name'], score=score_percentage)
    # order_by('-score') permet de trier les résultats par score, du plus grand au moins grand
    # La notation [:3] (opérateur "slice") renvoie les 3 premiers éléments de la liste
    leaderboard = Result.objects.order_by('-score')[:3]

    return render(request, 'quiz/results.html', {
        'score': score_percentage,
        'title': rank['title'],
        'description': rank['description'],
        'leaderboard': leaderboard,
    })
