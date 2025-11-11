from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):

    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()

    set_word = 'про'
    count_books_include_word = 0
    count_genres_include_word = 0
    for book in Book.objects.all():
        if(book.title.lower().find(set_word) != -1):
            count_books_include_word += 1
            print(book.title)

    for genre in Genre.objects.all():
        if(genre.name.lower().find(set_word) != -1):
            count_genres_include_word += 1

    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'count_books_include_word':count_books_include_word, 'count_genres_include_word':count_genres_include_word},
    )