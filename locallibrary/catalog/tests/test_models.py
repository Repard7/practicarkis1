from django.test import TestCase

from catalog.models import Author, Book, BookInstance, Genre, Language


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label,'first name')

    def test_date_of_death_label(self):
        author=Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label,'Died')

    def test_first_name_max_length(self):
        author=Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEqual(expected_object_name,str(author))

    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(),'/catalog/author/1')

class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Book.objects.create()

    def test_title_label(self):
        book=Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label,'title')

    def test_isbn_label(self):
        book=Book.objects.get(id=1)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label,'ISBN')

    def test_summary_label(self):
        book=Book.objects.get(id=1)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label,'summary')

    def test_author_label(self):
        book=Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEqual(field_label,'author')

    def test_genre_label(self):
        book=Book.objects.get(id=1)
        field_label = book._meta.get_field('genre').verbose_name
        self.assertEqual(field_label,'genre')

    def test_language_label(self):
        book=Book.objects.get(id=1)
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label,'language')

    def test_title_max_length(self):
        book=Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length,200)

    def test_summary_max_length(self):
        book=Book.objects.get(id=1)
        max_length = book._meta.get_field('summary').max_length
        self.assertEqual(max_length,1000)

    def test_isbn_max_length(self):
        book=Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length,13)

    def test_get_absolute_url(self):
        book=Book.objects.get(id=1)
        self.assertEqual(book.get_absolute_url(),'/catalog/book/1')

class BookInstanceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_book = Book.objects.create(
            title='Test Book',
            summary='Test Summary'
        )
        cls.book_instance = BookInstance.objects.create(
            book=test_book,
            imprint='Test Imprint'
        )

    def test_imprint_label(self):
        field_label = self.book_instance._meta.get_field('imprint').verbose_name
        self.assertEqual(field_label,'imprint')

    def test_book_label(self):
        field_label = self.book_instance._meta.get_field('book').verbose_name
        self.assertEqual(field_label,'book')

    def test_due_back_label(self):
        field_label = self.book_instance._meta.get_field('due_back').verbose_name
        self.assertEqual(field_label,'due back')

    def test_borrower_label(self):
        field_label = self.book_instance._meta.get_field('borrower').verbose_name
        self.assertEqual(field_label,'borrower')

    def test_status_label(self):
        field_label = self.book_instance._meta.get_field('status').verbose_name
        self.assertEqual(field_label,'status')

    def test_imprint_max_length(self):
        max_length = self.book_instance._meta.get_field('imprint').max_length
        self.assertEqual(max_length,200)

    def test_status_max_length(self):
        max_length = self.book_instance._meta.get_field('status').max_length
        self.assertEqual(max_length,1)

class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name="Иван")

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label,'name')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length,200)

    def test_str_name(self):
        genre=Genre.objects.get(id=1)
        self.assertEqual(genre.name,str(genre))

class LanguageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name="russian")

    def test_name_label(self):
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEqual(field_label,'name')

    def test_name_max_length(self):
        language = Language.objects.get(id=1)
        max_length = language._meta.get_field('name').max_length
        self.assertEqual(max_length,200)

    def test_str_name(self):
        language=Language.objects.get(id=1)
        self.assertEqual(language.name,str(language))