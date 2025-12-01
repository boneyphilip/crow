# posts/views.py
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from .models import Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages

from .models import Post, Category
from .forms import PostForm


# ==================================================
# HOME PAGE — shows posts, handles simple form post
# ==================================================
def home(request):

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)

            # Assign author (fallback: first user)
            post.author = request.user if request.user.is_authenticated else User.objects.first()
            post.created_at = timezone.now()

            # CATEGORY LOGIC
            category_name = request.POST.get("category_name", "").strip()

            if category_name:
                category, created = Category.objects.get_or_create(
                    name=category_name)

                if created:
                    messages.success(
                        request, f"New category '{category_name}' created!")

                post.category = category

            # Save post
            post.save()

            messages.success(
                request, "Your post has been shared successfully!")
            return redirect("home")

    else:
        form = PostForm()

    posts = Post.objects.all().order_by("-created_at")

    return render(request, "posts/home.html", {
        "form": form,
        "posts": posts
    })


# ==================================================
# CREATE POST PAGE (The big UI page)
# ==================================================
@login_required
def create_post(request):
    return render(request, "posts/create_post.html")


# ==================================================
# NORMAL UPVOTE
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
# ADD COMMENT (Top-level comment)
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
            author=request.user if request.user.is_authenticated else User.objects.first(),
            content=content,
            parent=None
        )

        messages.success(request, "Comment added!")
        return redirect("home")

    return redirect("home")


# ==================================================
# ADD REPLY (One-level nested reply)
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
            author=request.user if request.user.is_authenticated else User.objects.first(),
            content=content,
            parent=parent_comment
        )

        messages.success(request, "Reply added!")
        return redirect("post_detail", post_id=post.id)

    return redirect("home")


# ==================================================
# POST DETAIL PAGE (Single Post Page)
# ==================================================


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "posts/post_detail.html", {"post": post})

# ==================================================
# AJAX VOTING (Upvote & Downvote)
# ==================================================


@csrf_exempt
def ajax_vote(request, post_id):

    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Login required"})

    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

    # Load JSON from request
    data = json.loads(request.body)
    action = data.get("action")

    post = get_object_or_404(Post, id=post_id)

    # Voting logic
    if action == "upvote":
        post.upvotes += 1
    elif action == "downvote":
        post.upvotes -= 1
    else:
        return JsonResponse({"success": False, "error": "Invalid action"}, status=400)

    post.save()

    return JsonResponse({
        "success": True,
        "upvotes": post.upvotes
    })


# = == == == == == == == == == == == == == == == == == == == == == == == == =#


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only author can edit
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect("post_detail", post_id=post.id)

    return render(request, "posts/edit_post.html", {"post": post})


# =================================================================================#


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only author can delete
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == "POST":
        post.delete()
        return redirect("home")

    return render(request, "posts/delete_post.html", {"post": post})

# ==================================================================================#


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Only author of comment can delete
    if comment.author != request.user:
        return HttpResponseForbidden("You cannot delete this comment.")

    post_id = comment.post.id
    comment.delete()

    return redirect("post_detail", post_id=post_id)

# ==================================================================================#


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Author check
    if comment.author != request.user:
        return HttpResponseForbidden("You cannot edit this comment.")

    if request.method == "POST":
        comment.content = request.POST.get("content")
        comment.save()
        return redirect("post_detail", post_id=comment.post.id)

    return render(request, "posts/edit_comment.html", {"comment": comment})
