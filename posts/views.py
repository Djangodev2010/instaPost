from django.shortcuts import render
from django.views.generic import *
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate 
from django.contrib.auth.models import User
from django.contrib import messages 


# Create your views here.

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

class CreatePostView(TemplateView):
    template_name = 'posts/create_post.html'
    
class PostDetailView(DetailView):
    template_name = 'posts/post_detail.html'
    model = Post
