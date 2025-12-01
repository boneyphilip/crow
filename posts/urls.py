
# Import path function (used to define routes)
from django.urls import path

# Import all views (functions that handle what happens when a route is visited)
from . import views

# ===============================================
# URL Patterns for the "posts" app
# These map each URL path to a function inside views.py
# ===============================================

urlpatterns = [

    # -----------------------------------------------
    #  Home Page
    # -----------------------------------------------
    # When user goes to http://127.0.0.1:8000/
    # Django will load the home() view inside views.py
    # This page shows all posts and has the "Create Post" form.
    path('', views.home, name='home'),

    # -----------------------------------------------
    #  Create Post Page
    # -----------------------------------------------
    path('create/', views.create_post, name='create_post'),

    # -----------------------------------------------
    #  NEW: Post Detail Page
    # -----------------------------------------------
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),

    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("comment/delete/<int:comment_id>/",
         views.delete_comment, name="delete_comment"),



    # -----------------------------------------------
    #  Normal Upvote (non-AJAX)
    # -----------------------------------------------
    # This version reloads the page after upvoting.
    # Example URL: /upvote/3/  (where 3 = post ID)
    # It runs the upvote_post() view.
    path('upvote/<int:post_id>/', views.upvote_post, name='upvote_post'),

    # -----------------------------------------------
    #  NEW: AJAX Vote (Upvote + Downvote)
    # -----------------------------------------------
    path("ajax/vote/<int:post_id>/", views.ajax_vote, name="ajax_vote"),


    # -----------------------------------------------
    #  Category Search API (AJAX)
    # -----------------------------------------------
    # Called automatically while typing in the "Category" input box.
    # Example URL: /categories/search/?q=tech
    # It returns a JSON list of similar categories (for live suggestions).
    path('categories/search/', views.search_categories, name='search_categories'),

    # -----------------------------------------------
    # ➕ AJAX Create Category API
    # -----------------------------------------------
    # When the user clicks "Create 'Cars' category" in the suggestion dropdown,
    # the frontend sends an AJAX POST request here.
    # This instantly creates the new category in the database.
    path('categories/create/', views.ajax_create_category,
         name='ajax_create_category'),

    # -----------------------------------------------
    #  Add Comment
    # -----------------------------------------------
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),

    # -----------------------------------------------
    #  Reply to Comment
    # -----------------------------------------------
    path("reply/<int:comment_id>/", views.reply_comment, name="reply_comment"),
]
