menu = [{'title': 'About', 'url_name': 'about'},
        {'title': 'Add Book', 'url_name': 'add_book'},
        {'title': 'Contact', 'url_name': 'contact'},
        ]


class DataMixin:
    title_page = None
    genre_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.genre_selected is not None:
            self.extra_context['genre_selected'] = self.genre_selected

    def get_mixin_context(self, context, **kwargs):
        context['genre_selected'] = None
        context.update(kwargs)
        return context
