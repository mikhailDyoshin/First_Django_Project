from curses.ascii import HT
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):

        """
            Returns the last 5 questions not including
            those to be published in the future
        """

        # Filter only questions with pub_date in the past
        last_five_past_questions = Question.objects.filter(
                pub_date__lte=timezone.now()
            )

        # Gather IDs of the questions that have one choice at least
        l = []
        for q in last_five_past_questions:
            chs = q.choice_set.all()
            if chs:
                l.append(q.id)

        # Filter only questions with choices and take the last 5 of them
        questions_with_choices = last_five_past_questions.filter(
            id__in=l
        ).order_by('-pub_date')[:5]

        return questions_with_choices


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
            Excludes any question that isn't published yet
            or has no choices.
        """

        # Filter only questions with pub_date in the past
        past_questions = Question.objects.filter(pub_date__lte=timezone.now())

        # Gather IDs of the questions that have one choice at least
        l = []
        for q in past_questions:
            chs = q.choice_set.all()
            if chs:
                l.append(q.id)

        # Filter only questions with choices
        questions_with_choices = past_questions.filter(id__in=l)

        return questions_with_choices


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
            Excludes results of any question
            that isn't published yet.
        """

        return Question.objects.filter(pub_date__lte=timezone.now())


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
