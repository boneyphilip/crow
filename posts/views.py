# posts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from .forms import PostForm  # Import our new form
from django.http import JsonResponse  # Needed to send JSON data back to JS
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
            # Create a Post object but don’t save yet
            post = form.save(commit=False)
            # Assign author (use logged-in user, fallback to first user)
            post.author = request.user if request.user.is_authenticated else User.objects.first()
            post.created_at = timezone.now()  # Set the current time as creation time
           
             # -----------------------------
            # SMART CATEGORY CREATION LOGIC
            # -----------------------------
            # Get the category name from the form (either dropdown or search box)
            category_input = request.POST.get('category_name') or request.POST.get('category')

            # If the user typed or selected a category
            if category_input:
                # Try to find existing category (case insensitive)
                # If not found, create a new one automatically
                category_obj, created = Category.objects.get_or_create(
                    name__iexact=category_input,  # Search ignoring case
                    defaults={'name': category_input}  # If not found, create with this name
                )

                # Attach that category object to the post
                post.category = category_obj

            # Save post to database
            post.save()

            # After saving, reload page to clear form and show new post
            return redirect('home')

    else:
        # If the user just opened the page (GET request), show an empty form
        form = PostForm()

    # Fetch all posts from newest to oldest
    posts = Post.objects.all().order_by('-created_at')

    # Pass both form and posts to the HTML template
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

    # Convert the results into a simple list of names
    results = list(categories.values_list('name', flat=True))

    # Send the list back as JSON data (used by JavaScript)
    return JsonResponse({'results': results})