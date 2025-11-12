
from django import forms
from .models import Post

# This class defines how the Post form looks and works.
# It connects directly to the Post model.


class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # Link this form to the Post model
        fields = ['title', 'content']  # Fields that appear in the form

        # Optional: Add placeholder text and basic CSS styling
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a catchy title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts...'
            }),
        }
