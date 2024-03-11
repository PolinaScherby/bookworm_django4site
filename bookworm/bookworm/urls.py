from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from books.views import page_not_found

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('auth/', include('users.urls', namespace='users')),
]

handler404 = page_not_found

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
