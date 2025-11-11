from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.views import generic
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):

    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    set_word = 'про'
    count_books_include_word = 0
    count_genres_include_word = 0
    for book in Book.objects.all():
        if(book.title.lower().find(set_word) != -1):
            count_books_include_word += 1

    for genre in Genre.objects.all():
        if(genre.name.lower().find(set_word) != -1):
            count_genres_include_word += 1

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_visits': num_visits, 'count_books_include_word':count_books_include_word, 'count_genres_include_word':count_genres_include_word},)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
    model = Author

from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def loaned_books_by_user_list(request):
    # Проверяем есть ли права can_mark_returned
    if request.user.has_perm('catalog.can_mark_returned'):
        # Если есть права - показываем ВСЕ взятые книги
        book_list = BookInstance.objects.filter(
            status__exact='o'
        ).order_by('due_back')
    else:
        # Если нет прав - показываем только книги текущего пользователя
        book_list = BookInstance.objects.filter(
            borrower=request.user
        ).filter(
            status__exact='o'
        ).order_by('due_back')

    # Настраиваем пагинацию
    paginator = Paginator(book_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'catalog/bookinstance_list_borrowed_user.html',
        {'page_obj': page_obj, 'bookinstance_list': page_obj.object_list}
    )