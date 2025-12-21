from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

import json

from .forms import PostForm
from .models import Category, Comment, Post, PostMedia, Vote


# ==================================================
# HOME PAGE
# ==================================================
def home(request):
    form = PostForm()

    # ----- CREATE POST FROM HOME (optional) -----
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.author = request.user
            else:
                post.author = User.objects.first()
            post.created_at = timezone.now()

            category_name = request.POST.get("category", "").strip()
            if category_name:
                category, _ = Category.objects.get_or_create(
                    name=category_name)
                post.category = category

            post.save()
            messages.success(
                request, "Your post has been shared successfully!")
            return redirect("home")

    # ----- SEARCH -----
    query = request.GET.get("q", "").strip()
    if query:
        posts = Post.objects.filter(
            title__icontains=query).order_by("-created_at")
    else:
        posts = Post.objects.all().order_by("-created_at")

    # ----- USER VOTE STATE FOR UI -----
    for post in posts:
        post.user_vote_value = post.user_vote(request.user)

    return render(
        request,
        "posts/home.html",
        {
            "form": form,
            "posts": posts,
        },
    )


# ==================================================
# CREATE POST PAGE
# ==================================================
@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        category_name = request.POST.get("category", "").strip()

        if not title or not content:
            messages.error(request, "Title and content are required.")
            return redirect("create_post")

        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)

        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            category=category,
        )

        for img in request.FILES.getlist("images"):
            PostMedia.objects.create(post=post, file=img)

        if request.FILES.get("video"):
            PostMedia.objects.create(post=post, file=request.FILES["video"])

        for src in request.FILES.getlist("sources"):
            PostMedia.objects.create(post=post, file=src)

        messages.success(request, "Post created successfully!")
        return redirect("home")

    return render(request, "posts/create_post.html")


# ==================================================
# POST DETAIL
# ==================================================
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.user_vote_value = post.user_vote(request.user)
    return render(request, "posts/post_detail.html", {"post": post})


# ==================================================
# VOTING (AJAX – SINGLE SOURCE OF TRUTH)
# ==================================================
@login_required
def vote_post(request, post_id):
    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)

    post = get_object_or_404(Post, id=post_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "error": "Invalid JSON"},
            status=400,
        )

    action = data.get("action")
    if action not in ("upvote", "downvote"):
        return JsonResponse(
            {"success": False, "error": "Invalid action"},
            status=400,
        )

    value = 1 if action == "upvote" else -1

    vote, created = Vote.objects.get_or_create(
        user=request.user,
        post=post,
        defaults={"value": value},
    )

    if not created:
        if vote.value == value:
            vote.delete()  # Same vote clicked again => remove
        else:
            vote.value = value  # Switch upvote <-> downvote
            vote.save()

    return JsonResponse(
        {
            "success": True,
            "score": post.get_score(),
            "user_vote": post.user_vote(request.user),  # ✅ important for UI
        }
    )


# ==================================================
# COMMENTS
# ==================================================
@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get("content", "").strip()

        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
            )

    return redirect("post_detail", post_id=post_id)


@login_required
def reply_comment(request, comment_id):
    parent = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            Comment.objects.create(
                post=parent.post,
                author=request.user,
                content=content,
                parent=parent,
            )
    return redirect("post_detail", post_id=parent.post.id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden()
    post_id = comment.post.id
    comment.delete()
    return redirect("post_detail", post_id=post_id)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        comment.content = request.POST.get("content", "")
        comment.save()
        return redirect("post_detail", post_id=comment.post.id)

    return render(request, "posts/edit_comment.html", {"comment": comment})


# ==================================================
# EDIT / DELETE POST
# ==================================================
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        post.title = request.POST.get("title", "")
        post.content = request.POST.get("content", "")
        post.save()
        return redirect("post_detail", post_id=post.id)

    return render(request, "posts/edit_post.html", {"post": post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        post.delete()
        return redirect("home")

    return render(request, "posts/delete_post.html", {"post": post})


# ==================================================
# AUTH
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
# SEARCH (AJAX)
# ==================================================
def ajax_search(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"results": []})

    posts = Post.objects.filter(
        Q(title__icontains=q) | Q(author__username__icontains=q)
    ).select_related("author")

    results = []
    for post in posts:
        thumb = None
        if post.media.exists() and post.media.first().is_image():
            thumb = post.media.first().file.url

        results.append(
            {
                "id": post.id,
                "title": post.title,
                "author": post.author.username,
                "thumb": thumb,
            }
        )

    return JsonResponse({"results": results})


# ==================================================
# PROFILE
# ==================================================
def profile_page(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by("-created_at")
    return render(
        request,
        "posts/profile.html",
        {"profile_user": profile_user, "posts": posts},
    )


# ==================================================
# CATEGORY SEARCH
# ==================================================
def category_search(request):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"results": []})

    categories = Category.objects.filter(name__icontains=q)[:6]
    return JsonResponse({"results": [c.name for c in categories]})
