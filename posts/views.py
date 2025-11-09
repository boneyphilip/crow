# posts/views.py
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

# Home page view
def home(request):
    # Get all posts from the database (latest first)
    posts = Post.objects.all().order_by('-id')

    # If user submitted form
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()  # Save post to DB
            return redirect('/')  # reload home page
    else:
        form = PostForm()  # empty form

    # This line must be inside the function (indented)
    return render(request, 'posts/home.html', {'posts': posts, 'form': form})
