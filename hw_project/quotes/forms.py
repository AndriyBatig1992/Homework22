from django.forms import ModelForm
from .models import Tag, Quote
from django import forms


class TagForm(ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']



