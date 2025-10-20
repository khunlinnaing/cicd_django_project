from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """
    Post model အတွက် form
    - title, content field အတွက် user input လက်ခံ
    """
    class Meta:
        model = Post
        fields = ['title', 'content']  # Form မှာ အသုံးပြုမယ့် fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter content'}),
        }
        labels = {
            'title': 'ခေါင်းစဉ်',
            'content': 'အကြောင်းအရာ',
        }

