from django import forms
from .models import Post

# Custom Django form for Post model
class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # Connect to Post model
        fields = ['title', 'content']  # Fields visible on the form

        # Add Bootstrap styling to each field
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',  # Bootstrap style
                'placeholder': 'Enter your post title here...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',  # Bootstrap textarea style
                'rows': 5,
                'placeholder': 'Write your thoughts here...'
            }),
        }
