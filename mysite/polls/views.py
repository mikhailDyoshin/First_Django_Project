from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from django.template import loader

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
    return HttpResponse(f'You\'re looking at question {question_id}')


def results(request, question_id):
    responce = f'You\'re looing at the resulsts of  question {question_id}'
    return HttpResponse(responce)


def vote (request, question_id):
    return HttpResponse(f'You\'re voting on question {question_id}')
