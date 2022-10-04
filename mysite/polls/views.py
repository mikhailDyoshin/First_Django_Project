from curses.ascii import HT
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader
from django.http import Http404

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
    responce = f'You\'re looing at the resulsts of  question {question_id}'
    return HttpResponse(responce)


def vote (request, question_id):
    return HttpResponse(f'You\'re voting on question {question_id}')
