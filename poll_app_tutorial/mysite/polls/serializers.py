from rest_framework import serializers

from .models import Question
from .models import Choice


class QuestionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'was_published_recently']


class QuestionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'pub_date', 'question_text']


class ChoiceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['id', 'question', 'choice_text']


class ChoiceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']



