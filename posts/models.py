from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from cloudinary.models import CloudinaryField


# -----------------------------
# Category Model
# -----------------------------
class Category(models.Model):
    """Post category (e.g. News, Tech, Sports)."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return str(self.name)


# -----------------------------
# Post Model
# -----------------------------
class Post(models.Model):
    """Main post model."""

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

    def get_score(self) -> int:
        """
        Return total score based on Vote values (+1 / -1).
        Uses DB aggregation for performance.
        """
        total = self.votes.aggregate(total=Sum("value")).get("total")
        return int(total or 0)

    def user_vote(self, user) -> int:
        """
        Return current user's vote:
        +1 (upvote), -1 (downvote), 0 (no vote / anonymous)
        """
        if not user.is_authenticated:
            return 0

        vote = self.votes.filter(user=user).first()
        return int(vote.value) if vote else 0

    def __str__(self) -> str:
        return f"{self.title} by {self.author.username}"


# -----------------------------
# Vote Model (one vote per user per post)
# -----------------------------
class Vote(models.Model):
    """Stores a user's vote for a post (only once per post)."""

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

    def __str__(self) -> str:
        return (
            f"{self.user.username} voted {self.value} on Post {self.post.id}"
        )


# -----------------------------
# Comment Model
# -----------------------------
class Comment(models.Model):
    """Comments and replies (threaded)."""

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

    def __str__(self) -> str:
        if self.parent:
            return f"Reply by {self.author.username}"
        return f"Comment by {self.author.username}"


# -----------------------------
# Post Media Model
# -----------------------------
class PostMedia(models.Model):
    """Media files for a post (image, video, document)."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="media",
    )

    file = CloudinaryField(
        "media",
        resource_type="auto",
        blank=True,
        null=True,
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def is_image(self) -> bool:
        return self.file and self.file.resource_type == "image"

    def is_video(self) -> bool:
        return self.file and self.file.resource_type == "video"

    def is_document(self) -> bool:
        return self.file and self.file.resource_type == "raw"

    def __str__(self) -> str:
        return str(self.file)
