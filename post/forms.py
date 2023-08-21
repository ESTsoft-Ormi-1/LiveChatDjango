from django import forms
from .models import Post, HashTag


class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'content']


class HashTagForm(forms.ModelForm):
    
    class Meta:
        model = HashTag
        fields = ['name']