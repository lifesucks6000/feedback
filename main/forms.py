from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your name'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Share your thoughts with us',
            'rows': 4
        })
    )

    class Meta:
        model = Feedback
        fields = ['name', 'message']