from urllib import response
from venv import create
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question
import datetime

# q.choice_set.create(choice_text='Not much', votes=0)
def create_question(question_text, days):
    """
        Creates a question with the given "question_text"
        and published the given number of "days"
        offset to now
        (days < 0 for questions published in the past,
        days > 0 for questions that yet to be published.)
    """

    time = timezone.now() + datetime.timedelta(days=days)

    return Question.objects.create(question_text=question_text, pub_date=time)


def create_question_with_choice(question_text, days, choice):

    time = timezone.now() + datetime.timedelta(days=days)

    question_with_choice = Question.objects.create(
        question_text=question_text, pub_date=time
    )

    question_with_choice.choice_set.create(
        choice_text=choice,
        votes=0
    )

    return question_with_choice


# ********************Tests*for*was_published_recently********************
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        
        """
            was_published_recently()
            returns False
            for questions whose pub_date
            is in the future.
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_resently_with_old_question(self):

        """
            was_published_recently()
            returns False
            for questions whose pub_date
            is older then 1 day
        """

        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):

        """
            was_published_recently()
            return True
            for question whose pub_date
            is within the last day
        """

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


# ********************Tests*for*get_queryset*in*IndexView*class********************
class QuestionIndexViewTest(TestCase):

    def test_no_questions(self):
        """
            If no questions exist,
            an appropriate message is displayed
        """

        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_past_question(self):
        """
            Questions with a pub_date in the past
            and with choices
            are displayed on the index page.
        """

        question = create_question_with_choice(
            question_text="Past question", 
            days=-30, 
            choice='One'
        )

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )


    def test_future_question(self):
        """
            Questions with a pub_date in the future
            aren't displayed on the index page.
        """

        create_question("Future question", days=30)

        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [],
        )


    def test_future_question_and_past_question(self):
        """
            If both past and future questions exist,
            only past question with choices is displayed.
        """

        question = create_question_with_choice(
            question_text="Past question",
            days=-30,
            choice='One'
        )
        create_question("Future question", days=30)

        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    
    def test_two_past_question(self):
        """
            The index page may display multiple questions
            with choices.
        """

        question1 = create_question_with_choice(
            question_text="Past question 1",
            days = -30,
            choice='One'
        )

        question2 = create_question_with_choice(
            question_text="Past question 2",
            days = -5,
            choice='Two'
        )

        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1]
        )


    def test_question_without_choice(self):
        """
            The index page doesn't display questions without choices.
        """

        create_question("Question without choice", days=-5)
        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, "No polls are available")


    def test_question_with_choice(self):
        """
            The index page displays questions with choices.
        """

        question_with_choice = create_question_with_choice(
            question_text="Who", 
            days=-2, 
            choice="Dunno"
        )

        response = self.client.get(reverse('polls:index'))

        self.assertContains(response, question_with_choice.question_text)

# ********************Tests*for*get_queryset*in*DetailView*class********************
class QuestionDetailViewTest(TestCase):

    def test_future_question(self):
        """
            The detail view of a question
            which publication date is in the future
            returns a 404 not found.
        """

        future_question = create_question("Future question", days=5)

        url = reverse('polls:detail', args=(future_question.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


    def test_past_question(self):
        """
            The detail view of a question
            with the past publication date
            displays the question's text. 
        """

        past_question = create_question_with_choice(
            question_text="Past question",
            days=-5,
            choice='One'
        )

        url = reverse('polls:detail', args=(past_question.id,))

        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)


    def test_past_question_without_choice(self):
        """
            The detail view of a question
            with the past publication date
            but without a choice
            doesn't display the question's text. 
        """

        past_question_without_choice = create_question(
            question_text="Past question without choice",
            days = -5
        )

        url = reverse('polls:detail', 
            args=(past_question_without_choice.id,)
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        

# ********************Tests*for*get_queryset*in*ResultsView*class********************
class QuestionResultsView(TestCase):

    def test_future_question(self):
        """
            The results view of a question
            which publication date is in the future
            returns a 404 not found.
        """

        future_question = create_question("Future question", days=5)

        url = reverse('polls:results', args=(future_question.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


    def test_past_question_with_choice(self):
        """
            The results view of a question
            which publication date is in the past
            displays the question's choices and their votes
            if it has ones.
        """

        past_question = create_question_with_choice(
            question_text="Past question with choice",
            days=-5,
            choice='One'
        )

        url = reverse('polls:results', args=(past_question.id,))

        response = self.client.get(url)

        self.assertContains(response, past_question.question_text)


    def test_past_question_without_choice(self):
        """
            The results view of a question
            which publication date is in the past
            doesn't display the question's text
            if it hasn't choices.
        """

        past_question = create_question(
            question_text='Past question without choice',
            days = -2
        )

        url = reverse('polls:results', args=(past_question.id,))

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
