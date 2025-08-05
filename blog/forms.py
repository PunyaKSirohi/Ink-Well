from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }
        labels = {
            'content': 'Your Comment'
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL slug (auto-generated if left blank)'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 15,
                'placeholder': 'Write your post content here...'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'title': 'Post Title',
            'slug': 'URL Slug',
            'body': 'Content',
            'tags': 'Tags',
            'status': 'Status'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
