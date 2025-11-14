# posts/admin.py
from django.contrib import admin
# Import both models so we can show them in admin
from .models import Post, Category


# ----------------------------------------------
# CATEGORY ADMIN (for managing post categories)
# ----------------------------------------------
# This makes the Category section in admin look better and easier to use
class CategoryAdmin(admin.ModelAdmin):

    # These are the columns that will show up in the admin list
    list_display = ('name', 'post_count')

    # Add a small search bar at the top of admin to search by name
    search_fields = ('name',)

    # Sort the list automatically from A → Z
    ordering = ('name',)

    # Custom function to count how many posts belong to this category
    def post_count(self, obj):
        # "obj" here is a single Category (like "Science" or "News")
        # Django automatically connects Category to Post with post_set
        return obj.post_set.count()

    # Change the column name in admin to look friendly
    post_count.short_description = 'Number of Posts'


# ----------------------------------------------
# POST ADMIN (for managing user posts)
# ----------------------------------------------
# This improves the Post section in admin too
class PostAdmin(admin.ModelAdmin):

    # Show these columns in admin post list
    list_display = ('title', 'author', 'category', 'created_at', 'upvotes')

    # Add search bar so you can find posts by title or content
    search_fields = ('title', 'content')

    # Add filters (on right side in admin)
    list_filter = ('category', 'author')

    # Default sorting (latest first)
    ordering = ('-created_at',)


# ----------------------------------------------
# Register both models so they appear in admin
# ----------------------------------------------
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
