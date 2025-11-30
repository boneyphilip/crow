from django.db import models
from django.contrib.auth.models import User  # Import built-in User model


# -----------------------------
# Category Model
# -----------------------------
# This model represents categories like "News", "Technology", "Science", etc.
class Category(models.Model):
    # Each category must have a unique name
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        # When printed (like in admin), show the category name
        return self.name

# -----------------------------
# Post Model
# -----------------------------
# This model defines the structure of a Post in the database


class Post(models.Model):
    #  Author: who created the post (linked to Django's User table)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Add category field (each post belongs to one category)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)

    #  Title of the post
    title = models.CharField(max_length=200)

    #  Main content
    content = models.TextField()

    #  Automatically store date and time when created
    created_at = models.DateTimeField(auto_now_add=True)

    #  Count of upvotes (starts from 0)
    upvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        # When you print(Post), show title and author
        return f"{self.title} by {self.author.username}"

# -----------------------------
# Comment Model
# -----------------------------


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # NEW: parent comment for replies
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.parent:
            return f"Reply by {self.author.username}"
        return f"Comment by {self.author.username}"
