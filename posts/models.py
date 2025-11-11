from django.db import models
from django.contrib.auth.models import User  # Import built-in User model

# This model defines the structure of a Post in the database


class Post(models.Model):
    #  Author: who created the post (linked to Django's User table)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

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
