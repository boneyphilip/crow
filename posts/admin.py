# posts/admin.py
from django.contrib import admin
from .models import Post, Category, Vote


# ----------------------------------------------
# CATEGORY ADMIN
# ----------------------------------------------
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'post_count')
    search_fields = ('name',)
    ordering = ('name',)

    def post_count(self, obj):
        return obj.posts.count()

    post_count.short_description = 'Number of Posts'


# ----------------------------------------------
# POST ADMIN
# ----------------------------------------------
class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'category',
                    'score_display', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category', 'author')
    ordering = ('-created_at',)

    def score_display(self, obj):
        return obj.get_score()

    score_display.short_description = "Score"


# ----------------------------------------------
# REGISTER MODELS
# ----------------------------------------------
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Vote)
