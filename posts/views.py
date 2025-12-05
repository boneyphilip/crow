# posts/views.py
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import json

from .models import Post, PostMedia, Comment, Category
from .forms import PostForm


# ==================================================
# HOME PAGE — Shows posts & Handles search
# ==================================================
def home(request):

    # ----- POST Submission inside Home (optional form) -----
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user if request.user.is_authenticated else User.objects.first()
            post.created_at = timezone.now()

            # Category
            category_name = request.POST.get("category", "").strip()
            if category_name:
                category, created = Category.objects.get_or_create(
                    name=category_name)
                post.category = category
            post.save()

            messages.success(
                request, "Your post has been shared successfully!")
            return redirect("home")
    else:
        form = PostForm()

    # ----- SEARCH LOGIC -----
    query = request.GET.get("q", "")

    if query:
        posts = Post.objects.filter(
            title__icontains=query
        ).order_by("-created_at")
    else:
        posts = Post.objects.all().order_by("-created_at")

    return render(request, "posts/home.html", {
        "form": form,
        "posts": posts
    })


# ==================================================
# CREATE POST PAGE — Dedicated upload page
# ==================================================
@login_required
def create_post(request):

    if request.method == "POST":

        print("\n===== DEBUG: FILES RECEIVED =====")
        print("Images:", request.FILES.getlist("images"))
        print("Video:", request.FILES.get("video"))
        print("Sources:", request.FILES.getlist("sources"))
        print("ALL FILE KEYS:", request.FILES.keys())
        print("=================================\n")

        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        category_name = request.POST.get("category", "").strip()

        if not title or not content:
            messages.error(request, "Title and content are required.")
            return redirect("create_post")

        # Create category if needed
        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)

        # Create Post
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            category=category
        )

        # Save Images
        for img in request.FILES.getlist("images"):
            PostMedia.objects.create(post=post, file=img)

        # Save Video
        if request.FILES.get("video"):
            PostMedia.objects.create(post=post, file=request.FILES["video"])

        # Save Docs
        for src in request.FILES.getlist("sources"):
            PostMedia.objects.create(post=post, file=src)

        messages.success(request, "Post created successfully!")
        return redirect("home")

    return render(request, "posts/create_post.html")


# ==================================================
# NORMAL (NON-AJAX) UPVOTE
# ==================================================
def upvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.upvotes += 1
    post.save()
    return redirect("home")


# ==================================================
# CATEGORY LIVE SEARCH — AJAX
# ==================================================
def search_categories(request):
    query = request.GET.get("q", "").strip()

    categories = Category.objects.filter(name__icontains=query)
    results = list(categories.values_list("name", flat=True))

    exists = Category.objects.filter(name__iexact=query).exists()

    return JsonResponse({
        "results": results,
        "exists": exists,
        "typed": query,
    })


# ==================================================
# CREATE CATEGORY — AJAX
# ==================================================
def ajax_create_category(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if not name:
            return JsonResponse({"success": False, "error": "Empty name"}, status=400)

        category, created = Category.objects.get_or_create(name=name)

        return JsonResponse({
            "success": True,
            "created": created,
            "name": category.name,
        })

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


# ==================================================
# ADD COMMENT
# ==================================================
@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get("content", "").strip()

        if not content:
            messages.error(request, "Comment cannot be empty.")
            return redirect("home")

        Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            parent=None
        )

        return redirect("home")

    return redirect("home")


# ==================================================
# REPLY TO COMMENT
# ==================================================
@login_required
def reply_comment(request, comment_id):
    if request.method == "POST":
        parent_comment = get_object_or_404(Comment, id=comment_id)
        post = parent_comment.post
        content = request.POST.get("content", "").strip()

        if not content:
            messages.error(request, "Reply cannot be empty.")
            return redirect("post_detail", post_id=post.id)

        Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            parent=parent_comment
        )

        return redirect("post_detail", post_id=post.id)

    return redirect("home")


# ==================================================
# POST DETAIL PAGE
# ==================================================
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "posts/post_detail.html", {"post": post})


# ==================================================
# AJAX VOTING
# ==================================================
@csrf_exempt
def ajax_vote(request, post_id):

    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"})

    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

    data = json.loads(request.body)
    action = data.get("action")

    post = get_object_or_404(Post, id=post_id)

    if action == "upvote":
        post.upvotes += 1
    elif action == "downvote":
        post.upvotes -= 1
    else:
        return JsonResponse({"success": False, "error": "Invalid action"}, status=400)

    post.save()

    return JsonResponse({"success": True, "upvotes": post.upvotes})


# ==================================================
# EDIT POST
# ==================================================
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect("post_detail", post_id=post.id)

    return render(request, "posts/edit_post.html", {"post": post})


# ==================================================
# DELETE POST
# ==================================================
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden(
            "You are not allowed to delete this post."
        )

    if request.method == "POST":
        post.delete()
        return redirect("home")

    return render(request, "posts/delete_post.html", {"post": post})


# ==================================================
# DELETE COMMENT
# ==================================================
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden("You cannot delete this comment.")

    post_id = comment.post.id
    comment.delete()

    return redirect("post_detail", post_id=post_id)


# ==================================================
# EDIT COMMENT
# ==================================================
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden("You cannot edit this comment.")

    if request.method == "POST":
        comment.content = request.POST.get("content")
        comment.save()
        return redirect("post_detail", post_id=comment.post.id)

    return render(request, "posts/edit_comment.html", {"comment": comment})


# ==================================================
# REGISTER USER
# ==================================================
def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = UserCreationForm()

    return render(request, "posts/register.html", {"form": form})


# ==================================================
# AJAX SEARCH FOR NAV SEARCHBAR
# ==================================================
def ajax_search(request):
    q = request.GET.get("q", "").strip()

    if not q:
        return JsonResponse({"results": []})

    posts = Post.objects.filter(
        Q(title__icontains=q) |
        Q(author__username__icontains=q)
    ).select_related("author")

    result_list = []

    for p in posts:
        thumb = None
        if p.media.exists() and p.media.first().is_image:
            thumb = p.media.first().file.url

        result_list.append({
            "id": p.id,
            "title": p.title,
            "author": p.author.username,
            "thumb": thumb,
        })

    return JsonResponse({"results": result_list})


# =================================================
profile_page
# ==================================================


def profile_page(request, username):
    user_obj = get_object_or_404(User, username=username)

    posts = Post.objects.filter(author=user_obj).order_by("-created_at")

    return render(request, "posts/profile.html", {
        "profile_user": user_obj,
        "posts": posts
    })
