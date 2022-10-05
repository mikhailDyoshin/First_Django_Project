from curses.ascii import HT
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.db.models import F

def index(request):
    # Take 5 the latest questions in the system
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # Choose the template that will show the response
    template = loader.get_template('polls/index.html')

    # Form a context for the template (form the content for the html page)
    context = {
        'latest_question_list': latest_question_list,
    }

    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        # Take a question-object by its ID
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    
    # There is a shortcut for template rendering
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote (request, question_id):
    # Get an object of Question class with question_id ID
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choise = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choise.votes = F('votes') + 1
        selected_choise.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
