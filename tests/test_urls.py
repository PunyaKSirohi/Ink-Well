import pytest
from django.test import TestCase
from django.urls import reverse, resolve
from blog.views import PostListView, PostDetailView, add_comment


class TestBlogURLs:
    """Test cases for blog URL patterns"""
    
    def test_post_list_url(self):
        """Test post list URL pattern"""
        url = reverse('blog:post_list')
        assert url == '/'
        
        resolver = resolve(url)
        assert resolver.view_name == 'blog:post_list'
        assert resolver.func.view_class == PostListView
    
    def test_post_detail_url(self):
        """Test post detail URL pattern"""
        url = reverse('blog:post_detail', kwargs={'slug': 'test-post'})
        assert url == '/test-post/'
        
        resolver = resolve(url)
        assert resolver.view_name == 'blog:post_detail'
        assert resolver.func.view_class == PostDetailView
    
    def test_add_comment_url(self):
        """Test add comment URL pattern"""
        url = reverse('blog:add_comment', kwargs={'slug': 'test-post'})
        assert url == '/test-post/comment/'
        
        resolver = resolve(url)
        assert resolver.view_name == 'blog:add_comment'
        assert resolver.func == add_comment
    
    def test_admin_url(self):
        """Test admin URL is accessible"""
        url = reverse('admin:index')
        assert url == '/admin/'
