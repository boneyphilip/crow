# posts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt  # for AJAX create category

from .models import Post, Category
from .forms import PostForm


# -----------------------------
# Home page view
# Handles post creation + shows posts + adds success messages
# -----------------------------
def home(request):
    # If user submitted the form (POST request)
    if request.method == "POST":
        form = PostForm(request.POST)  # Bind the form with user input
        if form.is_valid():  # Validate form data
            # Create a Post object but don’t save yet
            post = form.save(commit=False)
            # Assign author (use logged-in user, fallback to first user)
            post.author = request.user if request.user.is_authenticated else User.objects.first()
            post.created_at = timezone.now()  # Set the current time as creation time

            # -----------------------------
            # SMART CATEGORY CREATION LOGIC
            # -----------------------------
            # Extract category name from the form
            category_name = request.POST.get('category_name')

            # If user entered a category
            if category_name:
                # Try to find it in database, or create a new one if not found
                category, created = Category.objects.get_or_create(name=category_name)

                # If category was newly created, show success message
                if created:
                    messages.success(request, f"New category '{category_name}' created!")

                # Assign the category to the post
                post.category = category

            # Save post to database
            post.save()

            # Show a success message for post creation
            messages.success(request, "Your post has been shared successfully!")

            # Redirect back to home to avoid form resubmission
            return redirect('home')

    else:
        # If just viewing the page, show empty form
        form = PostForm()

    # Fetch all posts from newest to oldest
    posts = Post.objects.all().order_by('-created_at')

    # Pass data to the template
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
    # Redirect back to homepage
    return redirect('home')


# -------------------------------------------
# AJAX upvote view
# This handles upvotes instantly (no reload)
# -------------------------------------------
def ajax_upvote_post(request, post_id):
    # Only accept POST requests for security
    if request.method == "POST":
        # Get the post safely (or 404 if not found)
        post = get_object_or_404(Post, id=post_id)

        # Increase the upvote count by 1
        post.upvotes += 1
        post.save()

        # Send back the updated count in JSON format
        return JsonResponse({"upvotes": post.upvotes})

    # If not a POST request, return an error
    return JsonResponse({"error": "Invalid request"}, status=400)


# -------------------------------------------
# Category Search API (AJAX)
# -------------------------------------------
def search_categories(request):
    # get the text user typed
    query = request.GET.get('q', '').strip()

    # find all categories that contain that word (case insensitive)
    categories = Category.objects.filter(name__icontains=query)

    # convert queryset to a simple list of names
    results = list(categories.values_list('name', flat=True))

    # check if the exact word already exists
    exists = Category.objects.filter(name__iexact=query).exists()

    # send all info as JSON back to the browser
    return JsonResponse({
        'results': results,   # all matching categories
        'exists': exists,     # True/False if exact match exists
        'typed': query        # what user typed
    })


# -----------------------------------------------------
# AJAX endpoint: Create a new category instantly
# -----------------------------------------------------
# CSRF handled safely via X-CSRFToken header in JS
def ajax_create_category(request):
    # Only accept POST requests
    if request.method == "POST":
        # Get the category name sent from JavaScript
        name = request.POST.get("name", "").strip()

        # Prevent empty category names
        if not name:
            return JsonResponse({"success": False, "error": "Empty name"}, status=400)

        # Try to find existing or create new
        category, created = Category.objects.get_or_create(name=name)

        # Send back response JSON
        return JsonResponse({
            "success": True,
            "created": created,        # True if newly created, False if it already existed
            "name": category.name
        })

    # If someone sends GET request → error
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
