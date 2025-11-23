
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
    #  Normal Upvote (non-AJAX)
    # -----------------------------------------------
    # This version reloads the page after upvoting.
    # Example URL: /upvote/3/  (where 3 = post ID)
    # It runs the upvote_post() view.
    path('upvote/<int:post_id>/', views.upvote_post, name='upvote_post'),

    # -----------------------------------------------
    #  AJAX Upvote (Instant)
    # -----------------------------------------------
    # This version uses JavaScript (no page reload).
    # The frontend JS calls this route with a POST request.
    # Example URL: /ajax/upvote/3/
    # It runs the ajax_upvote_post() view.
    path('ajax/upvote/<int:post_id>/',
         views.ajax_upvote_post, name='ajax_upvote_post'),

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
]
