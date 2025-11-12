from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from .forms import RenewBookForm

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

@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = '__all__'


class BookUpdate(UpdateView):
    model = Book
    fields = ['title','summary','language']


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')