from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/token/<int:token_id>/', views.post_list, name='post_list_by_token'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
]
