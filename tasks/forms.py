from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Task


class TaskForm(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=200)
    text = forms.CharField(label="Text", widget=forms.Textarea)
    published_date = forms.DateTimeField(
        label="Published Date",
        widget=forms.DateTimeInput(attrs={'class': 'datepicker'}),
        required=True
    )

    class Meta:
        model = Task
        fields = ['title', 'text', 'published_date']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if not title:
            self.add_error('title', 'Please enter a title.')
        if not text:
            self.add_error('text', 'Please enter some text.')

        return cleaned_data
