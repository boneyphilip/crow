from django.contrib import admin
from .models import Post, Category  # Import both models

# -----------------------------
# Register models for Django Admin
# -----------------------------
# This ensures both Post and Category appear in the admin panel.
admin.site.register(Post)
admin.site.register(Category)
