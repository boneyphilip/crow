from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm   # ✅ Import the styled form

def home(request):
    # Show all posts (latest first)
    posts = Post.objects.all().order_by('-id')

    # Check if form submitted
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # refresh after posting
    else:
        form = PostForm()  # blank form

    # Pass form + posts to HTML
    return render(request, 'posts/home.html', {'form': form, 'posts': posts})
