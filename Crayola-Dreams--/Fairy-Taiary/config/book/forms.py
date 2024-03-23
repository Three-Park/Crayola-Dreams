from django import forms
from .models import Book,Page

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_title','author', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 20,'style': 'resize: vertical;'}),
        }
        required = {
            'book_title': True,
            'author': True,
        }

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['book_id', 'diary_id', 'page_num']