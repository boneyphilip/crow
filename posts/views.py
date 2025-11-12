# posts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm  # Import our new form
from django.contrib.auth.models import User
from django.utils import timezone


# -----------------------------
# Home page view
# Shows all posts + handles new post form
# -----------------------------
def home(request):
    # If user submitted the form (POST request)
    if request.method == "POST":
        form = PostForm(request.POST)  # Bind the form with user input
        if form.is_valid():  # Validate form data
            post = form.save(commit=False)  # Create a Post object but don’t save yet
            # Assign author (use logged-in user, fallback to first user)
            post.author = request.user if request.user.is_authenticated else User.objects.first()
            post.created_at = timezone.now()  # Set current time
            post.save()  # Finally save to database
            return redirect('home')  # Reload the home page

    else:
        # If the user just opened the page, show empty form
        form = PostForm()

    # Fetch all posts from newest to oldest
    posts = Post.objects.all().order_by('-created_at')

    # Pass posts and form to template
    return render(request, 'posts/home.html', {'form': form, 'posts': posts})


# -----------------------------
# Upvote View
# Increases upvote count by +1 when user clicks the button
# -----------------------------
def upvote_post(request, post_id):
    # Fetch post by ID, or show 404 if not found
    post = get_object_or_404(Post, id=post_id)
    # Increase upvotes by 1
    post.upvotes += 1
    post.save()
    # Redirect back to home
    return redirect('home')
