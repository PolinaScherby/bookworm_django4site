from django import template

from books.models import Genre

register = template.Library()


@register.inclusion_tag('books/list_genres.html')
def show_genres(genre_selected=0):
    genres = Genre.objects.all()
    return {'genres': genres, 'genre_selected': genre_selected}


@register.filter(name='get_last_review')
def get_last_review(book):
    last_review = book.reviews.order_by('-time_create').first()
    return last_review
