from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('token/<int:token_id>/', views.post_list, name='post_list_by_token'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
]
