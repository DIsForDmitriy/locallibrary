from django.shortcuts import render
from django.views import generic

from catalog.models import Author, Book, BookInstanse, Genre
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    num_books = Book.objects.all().count()
    num_instanse = BookInstanse.objects.all().count()
    num_instanse_available = BookInstanse.objects.filter(status__exact='a').count()
    num_books_title = Book.objects.filter(title__icontains='').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.all().count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    return render(
        request,
        'index.html',
        context = {
            'num_books': num_books,
            'num_instanse': num_instanse, 
            'num_authors': num_authors, 
            'num_instanse_available': num_instanse_available,
            'num_genres': num_genres,
            'num_books_title': num_books_title,
            'num_visits': num_visits
            }
    )

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

    

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstanse
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstanse.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')