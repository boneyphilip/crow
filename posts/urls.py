
from django.urls import path
from . import views  # Import our views from posts app

urlpatterns = [
    # Home page that lists posts and has the post form
    path('', views.home, name='home'),

    # Normal (non-AJAX) upvote URL – still works as backup
    path('upvote/<int:post_id>/', views.upvote_post, name='upvote_post'),

    # AJAX upvote URL — will be called by JavaScript
    path('ajax/upvote/<int:post_id>/',
         views.ajax_upvote_post, name='ajax_upvote_post'),
    
    # NEW: Category Search API
    path('categories/search/', views.search_categories, name='search_categories'),
]
