from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    
    path('logout/', views.logout_view, name='logout'),
    
    path('register/', views.register, name='register'),
    
    path('login/', views.login_view, name='login'),
   
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail')
    
]
