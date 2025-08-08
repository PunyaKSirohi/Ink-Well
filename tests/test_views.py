import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Comment
from tests.factories import UserFactory, PostFactory, CommentFactory, DraftPostFactory


@pytest.mark.django_db
class TestPostViews:
    """Test cases for Post views"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = Client()
    
    def test_post_list_view_published_posts_only(self):
        """Test post list shows only published posts"""
        published_post = PostFactory(title="Published Post", status=1)
        draft_post = DraftPostFactory(title="Draft Post", status=0)
        
        response = self.client.get(reverse('blog:post_list'))
        
        assert response.status_code == 200
        assert "Published Post" in response.content.decode()
        assert "Draft Post" not in response.content.decode()
    
    def test_post_list_view_empty(self):
        """Test post list view when no posts exist"""
        response = self.client.get(reverse('blog:post_list'))
        
        assert response.status_code == 200
        assert "No posts available" in response.content.decode()
    
    def test_post_list_view_context(self):
        """Test post list view context data"""
        PostFactory.create_batch(3, status=1)
        
        response = self.client.get(reverse('blog:post_list'))
        
        assert response.status_code == 200
        assert 'posts' in response.context
        assert response.context['posts'].count() == 3
    
    def test_post_list_pagination(self):
        """Test post list pagination"""
        # Create more posts than paginate_by limit (5)
        PostFactory.create_batch(7, status=1)
        
        response = self.client.get(reverse('blog:post_list'))
        
        assert response.status_code == 200
        assert response.context['is_paginated'] is True
        assert len(response.context['posts']) == 5
    
    def test_post_detail_view_published_post(self):
        """Test post detail view for published post"""
        post = PostFactory(title="Test Post", slug="test-post", status=1)
        
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'test-post'}))
        
        assert response.status_code == 200
        assert "Test Post" in response.content.decode()
        assert response.context['post'] == post
    
    def test_post_detail_view_draft_post_404(self):
        """Test post detail view returns 404 for draft posts"""
        draft = DraftPostFactory(slug="draft-post", status=0)
        
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'draft-post'}))
        
        assert response.status_code == 404
    
    def test_post_detail_view_nonexistent_post_404(self):
        """Test post detail view returns 404 for non-existent post"""
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'nonexistent'}))
        
        assert response.status_code == 404
    
    def test_post_detail_view_with_comments(self):
        """Test post detail view displays comments"""
        post = PostFactory(status=1)
        comment1 = CommentFactory(post=post, content="First comment", active=True)
        comment2 = CommentFactory(post=post, content="Second comment", active=True)
        inactive_comment = CommentFactory(post=post, content="Inactive comment", active=False)
        
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': post.slug}))
        
        assert response.status_code == 200
        assert "First comment" in response.content.decode()
        assert "Second comment" in response.content.decode()
        assert "Inactive comment" not in response.content.decode()
    
    def test_post_detail_view_comment_count(self):
        """Test post detail view shows correct comment count"""
        post = PostFactory(status=1)
        CommentFactory.create_batch(3, post=post, active=True)
        CommentFactory(post=post, active=False)  # Inactive comment
        
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': post.slug}))
        
        assert response.status_code == 200
        assert response.context['comments'].count() == 3


@pytest.mark.django_db
class TestCommentViews:
    """Test cases for Comment views"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = Client()
        self.user = UserFactory()
        self.post = PostFactory(status=1)
    
    def test_add_comment_authenticated_user(self):
        """Test authenticated user can add comment"""
        self.client.force_login(self.user)
        
        comment_data = {
            'content': 'This is a test comment'
        }
        
        response = self.client.post(
            reverse('blog:add_comment', kwargs={'slug': self.post.slug}),
            data=comment_data
        )
        
        assert response.status_code == 302  # Redirect after success
        assert Comment.objects.filter(
            post=self.post,
            author=self.user,
            content='This is a test comment'
        ).exists()
    
    def test_add_comment_unauthenticated_user(self):
        """Test unauthenticated user cannot add comment"""
        comment_data = {
            'content': 'This is a test comment'
        }
        
        response = self.client.post(
            reverse('blog:add_comment', kwargs={'slug': self.post.slug}),
            data=comment_data
        )
        
        assert response.status_code == 302  # Redirect to login
        assert not Comment.objects.filter(
            post=self.post,
            content='This is a test comment'
        ).exists()
    
    def test_add_comment_invalid_data(self):
        """Test adding comment with invalid data"""
        self.client.force_login(self.user)
        
        comment_data = {
            'content': ''  # Empty content
        }
        
        response = self.client.post(
            reverse('blog:add_comment', kwargs={'slug': self.post.slug}),
            data=comment_data
        )
        
        # Should stay on the same page with errors
        assert response.status_code == 200
        assert not Comment.objects.filter(post=self.post, author=self.user).exists()
