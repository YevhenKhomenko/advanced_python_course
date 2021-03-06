import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(verbose_name='Question Text', max_length=200)
    pub_date = models.DateTimeField(verbose_name='Pub date')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name='Question', on_delete=models.CASCADE)
    choice_text = models.CharField(verbose_name='Choice Text', max_length=200)
    votes = models.IntegerField(verbose_name='Votes', default=0)

    def __str__(self):
        return '{} for {}'.format(self.choice_text, self.question)

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'


class ChoiceWithGoodMarks(models.Model):
    question = models.ForeignKey(Question, verbose_name='Question', related_name='good_marks', on_delete=models.CASCADE)
    choice_text = models.CharField(verbose_name='Choice Text', max_length=200)
    votes = models.IntegerField(verbose_name='Votes', default=0)

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'

