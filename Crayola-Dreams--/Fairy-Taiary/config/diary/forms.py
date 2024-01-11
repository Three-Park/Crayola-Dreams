from django import forms
from .models import Diary

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'content', 'image_url']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 20,'style': 'resize: vertical;'}),
        }
