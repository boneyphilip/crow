from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.utils import timezone

# -----------------------------
# Home page view
# Shows all posts + handles new post form
# -----------------------------


def home(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Author = currently logged-in user (temporary fallback to admin for now)
        author = request.user if request.user.is_authenticated else User.objects.first()

        # Create new post in database
        Post.objects.create(title=title, content=content,
                            author=author, created_at=timezone.now())

        # Redirect to home page after saving
        return redirect('home')

    # Fetch all posts (latest first)
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts})


# -----------------------------
# Upvote View
# Increases upvote count by +1 when user clicks the button
# -----------------------------
def upvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.upvotes += 1
    post.save()
    return redirect('home')
