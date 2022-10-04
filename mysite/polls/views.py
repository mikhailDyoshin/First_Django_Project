from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

def index(request):
    # Take 5 the latest questions in the system
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # Form the responce
    output = '; '.join([q.question_text for q in latest_question_list])

    return HttpResponse(output)


def detail(request, question_id):
    return HttpResponse(f'You\'re looking at question {question_id}')


def results(request, question_id):
    responce = f'You\'re looing at the resulsts of  question {question_id}'
    return HttpResponse(responce)


def vote (request, question_id):
    return HttpResponse(f'You\'re voting on question {question_id}')
