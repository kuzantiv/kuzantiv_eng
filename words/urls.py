from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('words/practice/', views.practice_words, name='practice_words'),
    path('add_word/', views.add_word, name='add_word'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('learned_word/<int:word_id>/', views.learned_word, name='learned_word'),
    path('manage_words/', views.manage_words, name='manage_words'),
    path('delete_word/<int:word_id>/', views.delete_word, name='delete_word'),
]
