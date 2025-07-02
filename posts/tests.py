from django.test import TestCase
from posts.models import *
from django.contrib.auth.models import User

# Create your tests here.

class AccountTest(TestCase):
    def setup(self):
        user = User.objects.create_user(username='test user', email='test@test.com', password='test')
        account = Account.objects.create(user=user, name=user.username,posts=None)
        print(account.user)
    
        
