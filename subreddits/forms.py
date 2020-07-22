from django import forms
from django.forms import Textarea
from .models import Subreddit, Comment


class SubrForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)

    def clean(self):
        name = self.cleaned_data["name"]
        if not name or len(name) > 30:
            raise forms.ValidationError(
                "Please enter a valid name(must be under 30 characters).")
        if Subreddit.objects.filter(name=name).exists():
            raise forms.ValidationError('Subreddit already exists')


class PostForm(forms.Form):
    name = forms.CharField(label='Post Name', max_length=100)
    text = forms.CharField(label='Text', max_length=255)

    def clean(self):
        name = self.cleaned_data["name"]
        if not name or len(name) > 100:
            raise forms.ValidationError(
                "Please enter a valid post name(must be under 100 characters).")


class CommentForm(forms.Form):
    text = forms.CharField(label='Text', max_length=255,
                           widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = 'Enter your comment here..'

    def clean(self):
        text = self.cleaned_data["text"]
        if not text or len(text) > 255:
            raise forms.ValidationError(
                "Please enter a valid comment(must be under 255 characters).")
