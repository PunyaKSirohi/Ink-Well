from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.text import slugify
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm, PostForm

# Create your views here.

class PostListView(ListView):
    """Display a list of published blog posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        return Post.objects.filter(status=1).order_by('-created_at')

class PostDetailView(DetailView):
    """Display a single blog post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status=1)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status=1)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('blog:post_detail', slug=slug)
    
    return redirect('blog:post_detail', slug=slug)

@login_required
def create_post(request):
    """Create a new blog post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Auto-generate slug if not provided
            if not post.slug:
                post.slug = slugify(post.title)
                # Ensure slug is unique
                original_slug = post.slug
                counter = 1
                while Post.objects.filter(slug=post.slug).exists():
                    post.slug = f"{original_slug}-{counter}"
                    counter += 1
            
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_post(request, slug):
    """Edit an existing blog post"""
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, slug):
    """Delete a blog post"""
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted successfully!')
        return redirect('blog:user_posts')
    
    return render(request, 'blog/delete_post.html', {'post': post})

@login_required
def user_posts(request):
    """Display user's own posts (both published and drafts)"""
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/user_posts.html', {'posts': posts})
