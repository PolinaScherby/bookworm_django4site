from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from taggit.models import Tag

from .forms import AddBookForm, ReviewForm, ContactForm
from .models import Author, Book, Genre, Review
from .utils import DataMixin


class BookHome(DataMixin, ListView):
    template_name = 'books/index.html'
    context_object_name = 'books'
    title_page = 'All genres'
    genre_selected = 0
    paginate_by = 7

    def get_queryset(self):
        return Book.published.all()


class BookByTag(DataMixin, ListView):
    model = Book
    template_name = 'books/index.html'
    context_object_name = 'books'
    tag = None

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['tag'])
        return Book.published.all().filter(tags__slug=self.tag.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            title=f'Books by tag: #{self.tag.name}'
        )


class BookGenre(DataMixin, ListView):
    template_name = 'books/index.html'
    context_object_name = 'books'
    allow_empty = False

    def get_queryset(self):
        return Book.published.filter(
            genre__slug=self.kwargs['genre_slug']).prefetch_related('genre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = Genre.objects.get(slug=self.kwargs['genre_slug'])
        return self.get_mixin_context(
            context,
            title='Genre: ' + genre.title,
            genre_selected=genre.pk,
        )


class ShowAuthor(DataMixin, DetailView):
    model = Author
    template_name = 'books/author.html'
    slug_url_kwarg = 'author_slug'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.published.filter(author=context['author'])
        return self.get_mixin_context(
            context,
            title=context['author'].name,
            books=books
        )


# def editions(request, year):
#     if year > 2023:
#         return redirect('home')
#
#     return HttpResponse(f'Edition year: {year}')


class ShowBook(DataMixin, DetailView):
    template_name = 'books/book.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(book=self.object)
        return self.get_mixin_context(
            context,
            title=context['book'].title,
            reviews=reviews,
            book=context['book'],
            form=ReviewForm(),
            )

    def get_object(self, queryset=None):
        return get_object_or_404(Book.published, slug=self.kwargs[self.slug_url_kwarg])

    def post(self, request, *args, **kwargs):
        review = Review(text=request.POST.get('text'),
                        rating=request.POST.get('rating'),
                        user=self.request.user,
                        book=self.get_object())
        review.save()
        return self.get(self, request, *args, **kwargs)


class AddBook(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddBookForm
    template_name = 'books/addbook.html'
    title_page = 'Add a Book'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        w = form.save(commit=False)
        w.user = self.request.user
        return super().form_valid(form)


class About(DataMixin, TemplateView):
    template_name = 'books/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='About')


class ContactInfo(DataMixin, TemplateView):
    template_name = 'books/contact.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            return redirect(self.success_url)
        else:
            # If the form is not valid, re-render the template with the form and errors
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return self.get_mixin_context(context, title='Contact Us')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')
