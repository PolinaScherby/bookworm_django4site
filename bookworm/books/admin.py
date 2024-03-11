from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Author, Book, Genre, Review


class BookGenreInline(admin.TabularInline):
    model = Book.genre.through


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'first_published', 'get_html_image', 'time_create', 'time_update', 'average_rating', 'status', 'tag_list', 'user')
    list_display_links = ('title', )
    list_editable = ('status', )
    prepopulated_fields = {'slug': ('title', )}
    readonly_fields = ('get_html_image', 'time_create', 'time_update')
    ordering = ('id', )
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'author__name']
    list_filter = ['author__name', 'status', 'user']
    inlines = [BookGenreInline]
    exclude = ['genre']
    save_on_top = True

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def get_html_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")
        return 'No image'

    get_html_image.short_description = "Image miniature"

    @admin.action(description='Publish selected books')
    def set_published(self, request, queryset):
        count = queryset.update(status=Book.Status.PUBLISHED)
        if count > 1:
            self.message_user(request, f'{count} books were published')
        else:
            self.message_user(request, f'{count} book was published')

    @admin.action(description='Unpublish selected books')
    def set_draft(self, request, queryset):
        count = queryset.update(status=Book.Status.DRAFT)
        if count > 1:
            self.message_user(request, f'{count} books were withdrawn from publication!', messages.WARNING)
        else:
            self.message_user(request, f'{count} book was withdrawn from publication!', messages.WARNING)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title', )}
    ordering = ('title', )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_html_photo')
    list_display_links = ('id', 'name')
    readonly_fields = ('get_html_photo', )
    prepopulated_fields = {'slug': ('name', )}
    ordering = ('name', )

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")
        return 'No photo'

    get_html_photo.short_description = "Photo miniature"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'rating', 'time_create')
    list_display_links = ('id', )
