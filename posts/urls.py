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
    
    path('like-post/<int:pk>', views.like_post, name='like_post')
    
]
