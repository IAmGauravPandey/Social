from django.shortcuts import render,HttpResponse,get_object_or_404
from django.contrib import admin,auth
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from .forms import UserForm,EditProfile,ProfileForm,PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.contrib.auth import login,authenticate
from .models import UserProfile,Post,Friend


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# Create your views here.
def home(request):
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.image = form.cleaned_data['image']
            post.save()
            #image=request.FILES['image']
            print(post.image)
            return redirect('/')
        else:
            redirect('/')
    else:
        form=PostForm()
        posts=Post.objects.all().order_by('-date')
        users=User.objects.exclude(id=request.user.id)
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        args={'form':form,'posts':posts,'users':users,'friends': friends}
        return render(request,'accounts/home.html',args)

        
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request,pk=None):
    if pk:
        user=User.objects.get(pk=pk)
    else:
        user=request.user
    args={'user':user}
    return render(request,'accounts/profile.html',args)
@login_required
def edit(request):
    if request.method=="POST":
        form=EditProfile(request.POST,instance=request.user)
        form_profile=ProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form=EditProfile(instance=request.user)
        return render(request,'accounts/register.html',{'form':form})
@login_required
def password(request):
    if request.method=="POST":
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('profile')
        else:
            messages.error(request, ('Old and new Password cannot be same'))
            return redirect('http://127.0.0.1:3000/password/')
    else:
        form=PasswordChangeForm(user=request.user)
        return render(request,'accounts/register.html',{'form':form})

def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('/')


