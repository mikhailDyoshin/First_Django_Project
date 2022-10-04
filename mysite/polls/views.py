from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse(f'You\'re looking at question {question_id}')

def results(request, question_id):
    responce = f'You\'re looing at the resulsts of  question {question_id}'
    return HttpResponse(responce)

def vote (request, question_id):
    return HttpResponse(f'You\'re voting on question {question_id}')
