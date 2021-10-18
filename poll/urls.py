from django.urls import path

from . import views

app_name = 'poll'

urlpatterns = [
    path('poll_index/', views.poll_index, name="poll_index"),
    path('<int:question_id>/', views.poll_detail, name='poll_detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/result/', views.result, name='result'),
]