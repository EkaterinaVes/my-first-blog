from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import  permissions
from .permissions import IsAuthor

@login_required
def post_list(request):
    permission_classes = (IsAuthor,)
    author = User.objects.get(username=request.user)
    posts = Post.objects.filter(author=author).filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'myblog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
        permission_classes = (IsAuthor,)
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'myblog/post_detail.html', {'post': post})
        
@login_required
def post_new(request):
    permission_classes = (IsAuthor,)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myblog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    permission_classes = (IsAuthor,)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'myblog/post_edit.html', {'form': form})

def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.save()
            return redirect('post_list') 
    else:
        form = UserForm() 

    return render(request, 'myblog/create_user.html', {'form': form}) 
