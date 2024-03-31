from django import forms
from blog.models import Post


class PostingForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
# ---------------------------------- [edit] ---------------------------------- #
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'title': '제목',
            'text': '내용',
        }