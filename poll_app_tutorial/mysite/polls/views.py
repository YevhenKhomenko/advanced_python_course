from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics

from .models import Question
from .models import Choice
from .serializers import QuestionListSerializer, QuestionDetailSerializer
from .serializers import ChoiceListSerializer, ChoiceDetailsSerializer


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer


class QuestionDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionDetailSerializer

    def get_object(self):
        return get_object_or_404(Question, pk=self.kwargs.get('question_id'))


class ChoiceList(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceListSerializer


class ChoiceDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChoiceDetailsSerializer

    def get_object(self):
        return get_object_or_404(Choice, pk=self.kwargs.get('choice_id'))


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse("Latest questions: {}".format(output))


def detail(request, question_id):
    return HttpResponse("You are looking at question {}".format(question_id))


def results(request, question_id):
    return HttpResponse("You are looking at the results of question {}".format(question_id))


def vote(request, question_id):
    return HttpResponse("You are voting on question {}".format(question_id))


