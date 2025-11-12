from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upvote/<int:post_id>/', views.upvote_post, name='upvote_post'),
]
