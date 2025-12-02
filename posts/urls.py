from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [

    # ---------- HOME ----------
    path("", views.home, name="home"),

    # ---------- AUTH ----------
    path("login/", auth_views.LoginView.as_view(template_name="posts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register_user, name="register"),

    # ---------- SEARCH ----------
    path("search/ajax/", views.ajax_search, name="ajax_search"),

    # ---------- POSTS ----------
    path("create/", views.create_post, name="create_post"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),

    # ---------- VOTING ----------
    path("upvote/<int:post_id>/", views.upvote_post, name="upvote_post"),
    path("ajax/vote/<int:post_id>/", views.ajax_vote, name="ajax_vote"),

    # ---------- COMMENTS ----------
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("comment/delete/<int:comment_id>/",
         views.delete_comment, name="delete_comment"),
    path("comment/edit/<int:comment_id>/",
         views.edit_comment, name="edit_comment"),
    path("reply/<int:comment_id>/", views.reply_comment, name="reply_comment"),

    # ---------- CATEGORY (AJAX) ----------
    path("categories/search/", views.search_categories, name="search_categories"),
    path("categories/create/", views.ajax_create_category,
         name="ajax_create_category"),
]
