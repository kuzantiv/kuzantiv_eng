from django.contrib.auth.models import User
from django.db import models


class Word(models.Model):
    english_word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    transcription = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.english_word


class LearnedWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.word.english_word}'
