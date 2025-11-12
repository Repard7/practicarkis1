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
from django.contrib.auth.mixins import PermissionRequiredMixin
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
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

@login_required
def loaned_books_by_user_list(request):
    if request.user.has_perm('catalog.can_mark_returned'):
        book_list = BookInstance.objects.filter(
            status__exact='o'
        ).order_by('due_back')
    else:
        book_list = BookInstance.objects.filter(
            borrower=request.user
        ).filter(
            status__exact='o'
        ).order_by('due_back')

    paginator = Paginator(book_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'catalog/bookinstance_list_borrowed_user.html',
        {'page_obj': page_obj, 'bookinstance_list': page_obj.object_list}
    )

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}
    permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(UpdateView):
    model = Book
    fields = ['title','summary','language']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):

    book_inst=get_object_or_404(BookInstance, pk = pk)

    if request.method == 'POST':

        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('my-borrowed') )

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})