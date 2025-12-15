from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


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
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_score(self):
        """
        Return total post score based on votes.
        Uses database aggregation for performance.
        """
        return self.votes.aggregate(
            total=Sum("value")
        )["total"] or 0

    def __str__(self):
        return f"{self.title} by {self.author.username}"


# -----------------------------
# Vote Model (One vote per user per post)
# -----------------------------
class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1

    VOTE_CHOICES = (
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return (
            f"{self.user.username} voted "
            f"{self.value} on Post {self.post.id}"
        )


# -----------------------------
# Comment Model
# -----------------------------
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
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
        if self.parent:
            return f"Reply by {self.author.username}"
        return f"Comment by {self.author.username}"


# -----------------------------
# Post Media Model
# -----------------------------
class PostMedia(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="media",
    )
    file = models.FileField(upload_to="post_media/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def is_image(self):
        return self.file.name.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".webp")
        )

    def is_video(self):
        return self.file.name.lower().endswith(
            (".mp4", ".mov", ".avi", ".mkv")
        )

    def is_document(self):
        return not (self.is_image() or self.is_video())

    def __str__(self):
        return self.file.name
