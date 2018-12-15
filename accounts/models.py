from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class UserProfileManager(models.Model):
    def get_queryset(self):
        return super(UserProfileManager)
        self.get_queryset().filter(city='London')

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=100,default='')
    city=models.CharField(max_length=100,default='')
    website=models.URLField(default='')
    phone=models.IntegerField(default=0)
    image=models.ImageField(upload_to='profile_image',blank=True)
    london=UserProfileManager()

    def __str__(self):
        return self.user.username

def create_profile(sender,**kwargs):
    if kwargs['created']:
         user_profile=UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image=models.FileField(upload_to='post_image',blank=True)
    title = models.CharField(max_length=200)
    date=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

def create_post(sender,**kwargs):
    if kwargs['created']:
         user_post=Post.objects.create(user=kwargs['instance'])

post_save.connect(create_post,sender=User)

class Friend(models.Model):
    users=models.ManyToManyField(User)
    current_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner',null=True)

    @classmethod
    def make_friend(cls,current_user,new_friend):
        friends,created=cls.objects.get_or_create(
            current_user=current_user
        )
        friends.users.add(new_friend)

    @classmethod
    def lose_friend(cls,current_user,new_friend):
        friends,created=cls.objects.get_or_create(
            current_user=current_user
        )
        friends.users.remove(new_friend)