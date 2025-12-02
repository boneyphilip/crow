from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# Category Model
# -----------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# -----------------------------
# Post Model
# -----------------------------
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    upvotes = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author.username}"


# -----------------------------
# Comment Model
# -----------------------------
class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username}" if self.parent else f"Comment by {self.author.username}"


# -----------------------------
# Post Media Model (LAST)
# -----------------------------
class PostMedia(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="post_media/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def is_image(self):
        return self.file.name.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))

    def is_video(self):
        return self.file.name.lower().endswith((".mp4", ".mov", ".avi", ".mkv"))

    def is_document(self):
        return not (self.is_image() or self.is_video())

    def __str__(self):
        return self.file.name
