from django.urls import path
from . import views, auth_views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('register/', auth_views.register_view, name='register'),
    path('profile/', auth_views.profile_view, name='profile'),
    path('create/', views.create_post, name='create_post'),
    path('my-posts/', views.user_posts, name='user_posts'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
]
