from django.urls import path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.BookHome.as_view(), name='home'),
    path('tags/<str:tag>/', views.BookByTag.as_view(), name='books_by_tags'),
    path('addbook/', views.AddBook.as_view(), name='add_book'),
    path('book/<slug:book_slug>/', views.ShowBook.as_view(), name='book'),
    path('genre/<slug:genre_slug>/', views.BookGenre.as_view(), name='genre'),
    path('author/<slug:author_slug>/', views.ShowAuthor.as_view(), name='author'),
    # path('editions/<year4:year>/', views.editions, name='editions'),
    path('about/', views.About.as_view(), name='about'),
    path('contact/', views.ContactInfo.as_view(), name='contact'),
]
