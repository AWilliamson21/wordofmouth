from django import forms

class CommentForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    body = forms.Textarea()