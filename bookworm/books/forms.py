from django import forms

from .models import Book, Review


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'first_published', 'description', 'quote', 'image', 'tags', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w3-input'}),
            'author': forms.Select(attrs={'class': 'w3-select w3-border'}),
            'genre': forms.SelectMultiple(attrs={'cols': 50}),
            'first_published': forms.TextInput(attrs={'class': 'w3-input'}),
            'description': forms.Textarea(attrs={'class': 'w3-input', 'cols': 50, 'rows': 5, 'style': 'resize:none;'}),
            'quote': forms.Textarea(attrs={'class': 'w3-input', 'cols': 50, 'rows': 5, 'style': 'resize:none;'}),
            'tags': forms.TextInput(attrs={'class': 'w3-input'}),
            'slug': forms.TextInput(attrs={'class': 'w3-input'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'w3-input w3-border', 'rows': 5}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'w3-input',
        'placeholder': 'Your name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w3-input',
        'placeholder': 'Your email'
    }))
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w3-input',
        'cols': 50,
        'rows': 5,
        'placeholder': 'Please leave your feedback here...',
        }
    ))
