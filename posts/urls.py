from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [

    # ---------- HOME ----------
    path("", views.home, name="home"),

    # ---------- AUTH ----------
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="posts/login.html"
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register_user, name="register"),
    path("profile/<str:username>/", views.profile_page, name="profile_page"),

    # ---------- SEARCH ----------
    path("search/ajax/", views.ajax_search, name="ajax_search"),

    # ---------- POSTS ----------
    path("create/", views.create_post, name="create_post"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),

    # ---------- VOTING (FINAL, SINGLE SOURCE OF TRUTH) ----------
    path("ajax/vote/<int:post_id>/", views.vote_post, name="vote_post"),

    # ---------- COMMENTS ----------
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path(
        "comment/delete/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment",
    ),
    path(
        "comment/edit/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment",
    ),
    path("reply/<int:comment_id>/", views.reply_comment, name="reply_comment"),

    # ---------- CATEGORY ----------
    path(
        "categories/search/",
        views.category_search,
        name="category_search",
    ),
]
