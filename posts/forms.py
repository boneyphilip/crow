
from django import forms
from .models import Post, Category

# -----------------------------
# PostForm - used on the home page to create a new post
# -----------------------------
# This class defines how the Post form looks and works.
# It connects directly to the Post model.


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Include title, content, and category in the form
        fields = ['title', 'content', 'category']

        # Change how form fields look
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a catchy title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write something interesting...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        # Custom labels (just to make it friendlier)
        labels = {
            'title': 'Post Title',
            'content': 'Content',
            'category': 'Choose Category',
        }
