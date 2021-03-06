from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('question/', views.QuestionList.as_view(), name='QuestionList'),
    path('question/<int:question_id>/', views.QuestionDetails.as_view(), name='QuestionDetails'),
    path('choice/', views.ChoiceList.as_view(), name='ChoiceList'),
    #path('question/choices/', views.ChoiceList.as_view(), name='ChoiceList'),
    path('choice/<int:choice_id>/', views.ChoiceDetails.as_view(), name='ChoiceDetails'),
]
