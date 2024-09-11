import json
import random
import subprocess
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import WordForm
from .models import Word, LearnedWord

context = {
    'word': "",
    'translations': [],
    'chosen_word': None,
    'status': None
}


def home(request):
    return render(request, 'words/home.html')


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file', ''):
        uploaded_file = request.FILES['file']
        words_list = [[item.strip() for item in line.decode('utf-8').split(',')] for line in uploaded_file]
        #pprint(words_list)
        for item in words_list:
            w = Word(english_word=item[0], transcription=item[1], translation=item[2])
            w.save()
        return render(request, 'words/upload_file.html')
    return render(request, 'words/upload_file.html')


def practice_words(request):
    global context
    words = Word.objects.all()

    if request.method == "POST":
        print(request.POST.get("translation"))
        control_word, chosen_word = request.POST.get("translation").split(',')
        word_obj = Word.objects.filter(translation=chosen_word)
        context['chosen_word'] = chosen_word
        print(chosen_word)
        if word_obj and str(word_obj[0]) == control_word:
            context['status'] = True
            return render(request, 'words/practice_words.html', context)
        else:
            context['status'] = False
            return render(request, 'words/practice_words.html', context)

    if request.method == "GET":
        if words.exists():
            word = random.choice(words)
            translations = list(words.exclude(id=word.id).values_list('translation', flat=True))
            translations = random.sample(translations, min(3, len(translations)))  # Ensure we get 3 wrong translations
            translations.append(word.translation)
            random.shuffle(translations)
            context['status'] = None
            context['chosen_word'] = None
            context['word'] = word
            context['translations'] = translations
            return render(request, 'words/practice_words.html', context)

    else:
        return render(request, 'words/no_words.html')  # Handle case with no words


def no_words(request):
    return render(request, 'words/no_words.html')


@login_required
def add_word(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_word')
    else:
        form = WordForm()
    return render(request, 'words/add_word.html', {'form': form})


@login_required
def learned_word(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    LearnedWord.objects.get_or_create(user=request.user, word=word)
    return redirect('practice')


@login_required
def manage_words(request):
    words = Word.objects.all()
    return render(request, 'words/manage_words.html', {'words': words})


@login_required
def delete_word(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    word.delete()
    return redirect('manage_words')
