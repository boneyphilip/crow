# posts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from .forms import PostForm  # Import our new form
from django.http import JsonResponse  # Needed to send JSON data back to JS
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages  # Import Django messages framework

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
                category, created = Category.objects.get_or_create(
                    name=category_name)

                # If category was newly created, show success message
                if created:
                    messages.success(
                        request, f"New category '{category_name}' created!")

                # Assign the category to the post
                post.category = category

            # Save post to database
            post.save()

            # Show a success message for post creation
            messages.success(
                request, "Your post has been shared successfully!")

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
# This function will return matching categories as JSON
# Example: /categories/search/?q=tech  → returns ["Technology", "Tech News"]

def search_categories(request):
    # Get the text user typed in the search bar (example: ?q=tech)
    query = request.GET.get('q', '')

    # Find categories containing that text (case insensitive)
    categories = Category.objects.filter(name__icontains=query)

    # Convert the results into a simple list of names  (e.g. ["Tech", "Technology"])
    results = list(categories.values_list('name', flat=True))

    # Check if the exact typed word already exists
    already_exists = Category.objects.filter(name__iexact=query).exists()

    # Return both results and a flag for existence
    return JsonResponse({
        'results': results,
        'exists': already_exists,
        'typed': query,  # send back what user typed (for frontend use)
    })