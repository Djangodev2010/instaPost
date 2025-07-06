from django.shortcuts import render, get_object_or_404
from django.views.generic import *
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import logout, login, authenticate 
from django.contrib.auth.models import User
from django.contrib import messages 
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    template_name = 'posts/index.html'
    model = Post
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.all().order_by('-created_on')
    
def logout_view(request):
    logout(request)
    success_url = reverse('index')
    return HttpResponseRedirect(success_url)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        print(username, password, email)
        
        fail_url = reverse('register')
        success_url = reverse('login')
        
        if password != confirm_password:
            messages.error(request, 'Passwords Do Not Match!')
            return HttpResponseRedirect(fail_url)
        
        else:
            if User.objects.filter(username=username, email=email):
                messages.error(request, 'Username or Email Already Used!')
                
                return HttpResponseRedirect(fail_url)
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                print(username, password, email)
                user.save()
                account = Account(user=user, name=username)
                account.save()
                messages.success(request, 'Account Created Successfully!')
                return HttpResponseRedirect(success_url)
    else:
        return render(request, 'posts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        fail_url = reverse('login')
        success_url = reverse('index')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(success_url)
        
        else:
            messages.error(request, 'Invalid Credentials!')
            return HttpResponseRedirect(fail_url)

    else:
        return render(request, 'posts/login.html')

@method_decorator(login_required, name='dispatch')
def create_post(request):
    success_url = reverse('index')
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(user=user, title=title, content=content)
        return HttpResponseRedirect(success_url)

    else:
        return render(request, 'posts/create_post.html')

@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    template_name = 'posts/post_detail.html'
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(post=post)
        return context

@method_decorator(login_required, name='dispatch')
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.disliked_by.all():
        post.dislikes -= 1
        post.disliked_by.remove(request.user)
        post.save()
    
    if request.user in post.liked_by.all():
        post.likes -= 1
        post.liked_by.remove(request.user)
        post.save()
        return JsonResponse({'status': "unliked"})
    
    else:
        post.likes += 1
        post.liked_by.add(request.user)
        post.save()
        return JsonResponse({'status': "liked"})

@method_decorator(login_required, name='dispatch')
def dislike_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.liked_by.all():
        post.likes -= 1
        post.liked_by.remove(request.user)
        post.save()
    
    if request.user in post.disliked_by.all():
        post.dislikes -= 1
        post.disliked_by.remove(request.user)
        post.save()
        return JsonResponse({'status': "undisliked"})
    
    else:
        post.dislikes += 1
        post.disliked_by.add(request.user)
        post.save()
        return JsonResponse({'status': "disliked"})

@method_decorator(login_required, name='dispatch')
def save_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.saved_by.all():
        post.saved_by.remove(request.user)
        post.save()
        return JsonResponse({'status': 'unsaved'})
    
    else:
        post.saved_by.add(request.user)
        post.save()
        return JsonResponse({'status': 'saved'})

@method_decorator(login_required, name='dispatch')
def add_comment(request, pk):
    success_url = reverse('post_detail', kwargs={'pk': pk})
    if request.method == 'POST':
        post = get_object_or_404(Post, id=pk)
        content = request.POST.get('content')
        if Comment.objects.filter(user=request.user, post=post):
            messages.error(request, 'You already have a comment on this post!')
            return HttpResponseRedirect(success_url)
        else:
            comment = Comment.objects.create(user=request.user, content=content, post=post)
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return HttpResponseRedirect(success_url)
    
    else:
        return render(request, 'posts/add_comment.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):
    template_name = 'posts/profile.html'
    model = User
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user=self.request.user)
        return context

@method_decorator(login_required, name='dispatch')
def saved_posts(request, pk):
    user = get_object_or_404(User, id=pk)
    posts = Post.objects.filter(saved_by=user)
    return render(request, 'posts/index.html', {'posts': posts})

