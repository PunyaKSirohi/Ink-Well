import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Comment
from tests.factories import UserFactory, PostFactory, CommentFactory, DraftPostFactory


@pytest.mark.django_db
@pytest.mark.integration
class TestBlogWorkflow:
    """Integration tests for complete blog workflow"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = Client()
        self.user = UserFactory()
        self.admin_user = UserFactory(is_staff=True, is_superuser=True)
    
    def test_complete_blog_workflow(self):
        """Test complete blog workflow: create post, view, comment"""
        
        # 1. Admin creates a post
        self.client.force_login(self.admin_user)
        
        # Create post via admin (simulated)
        post = PostFactory(
            title="Integration Test Post",
            slug="integration-test-post",
            author=self.admin_user,
            status=1
        )
        
        # 2. Anonymous user views post list
        self.client.logout()
        response = self.client.get(reverse('blog:post_list'))
        assert response.status_code == 200
        assert "Integration Test Post" in response.content.decode()
        
        # 3. Anonymous user views post detail
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'integration-test-post'}))
        assert response.status_code == 200
        assert "Integration Test Post" in response.content.decode()
        
        # 4. User logs in and adds comment
        self.client.force_login(self.user)
        
        comment_data = {
            'content': 'Great post! Thanks for sharing.'
        }
        
        response = self.client.post(
            reverse('blog:add_comment', kwargs={'slug': 'integration-test-post'}),
            data=comment_data
        )
        
        assert response.status_code == 302  # Redirect after comment
        
        # 5. Verify comment appears on post
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'integration-test-post'}))
        assert response.status_code == 200
        assert "Great post! Thanks for sharing." in response.content.decode()
        
        # 6. Verify comment is in database
        comment = Comment.objects.get(
            post=post,
            author=self.user,
            content='Great post! Thanks for sharing.'
        )
        assert comment.active is True
    
    def test_draft_post_not_visible_to_public(self):
        """Test draft posts are not visible to public but visible to admin"""
        
        # Create draft post
        draft_post = DraftPostFactory(
            title="Draft Post",
            slug="draft-post",
            author=self.admin_user,
            status=0
        )
        
        # Anonymous user cannot see draft
        response = self.client.get(reverse('blog:post_list'))
        assert "Draft Post" not in response.content.decode()
        
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'draft-post'}))
        assert response.status_code == 404
        
        # Regular user cannot see draft
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'draft-post'}))
        assert response.status_code == 404
    
    def test_comment_moderation_workflow(self):
        """Test comment moderation workflow"""
        
        # Create post and comment
        post = PostFactory(status=1)
        comment = CommentFactory(post=post, active=False)  # Inactive comment
        
        # Comment should not appear on post detail
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': post.slug}))
        assert comment.content not in response.content.decode()
        
        # Admin can activate comment via admin panel (simulated)
        comment.active = True
        comment.save()
        
        # Now comment should appear
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': post.slug}))
        # Check for the content with linebreaks converted to <br> tags
        comment_html = comment.content.replace('\n', '<br>')
        assert comment_html in response.content.decode()
    
    def test_pagination_workflow(self):
        """Test pagination works correctly"""
        
        # Create 7 posts (more than paginate_by = 5)
        posts = PostFactory.create_batch(7, status=1)
        
        # First page should have 5 posts
        response = self.client.get(reverse('blog:post_list'))
        assert response.status_code == 200
        assert len(response.context['posts']) == 5
        assert response.context['is_paginated'] is True
        
        # Second page should have 2 posts
        response = self.client.get(reverse('blog:post_list') + '?page=2')
        assert response.status_code == 200
        assert len(response.context['posts']) == 2
    
    def test_user_authentication_workflow(self):
        """Test user authentication affects commenting"""
        
        post = PostFactory(status=1)
        
        # Anonymous user cannot comment
        comment_data = {'content': 'Anonymous comment'}
        response = self.client.post(
            reverse('blog:add_comment', kwargs={'slug': post.slug}),
            data=comment_data
        )
        
        assert response.status_code == 302  # Redirect to login
        assert not Comment.objects.filter(post=post).exists()
        
        # Authenticated user can comment
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('blog:add_comment', kwargs={'slug': post.slug}),
            data=comment_data
        )
        
        assert response.status_code == 302  # Redirect after success
        assert Comment.objects.filter(post=post, author=self.user).exists()
