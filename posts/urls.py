from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    
    path('logout/', views.logout_view, name='logout'),
    
    path('register/', views.register, name='register'),
    
    path('login/', views.login_view, name='login'),
   
    path('create-post/', views.create_post, name='create_post'),
    
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    
    path('like-post/<int:pk>', views.like_post, name='like_post'),
    
    path('dislike-post/<int:pk>/', views.dislike_post, name='like_post'),
    
    path('save-post/<int:pk>/', views.save_post, name='save_post'),
    
    path('add-comment/<int:pk>/', views.add_comment, name='add_comment'),
    
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    
    path('post/save-post/<int:pk>/', save_post, name='save_detail_post'),
    
    path('<int:pk>/saved-posts/', views.saved_posts, name='saved_posts')
    
]
