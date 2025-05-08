from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content', 'tags', 'image', 'link']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }

class SearchForm(forms.Form):
    query     = forms.CharField(required=False, label="Keyword")
    tags      = forms.CharField(required=False, label="Tags (comma-separated)")
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to   = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
