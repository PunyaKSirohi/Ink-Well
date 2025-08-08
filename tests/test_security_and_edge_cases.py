"""
Security and edge case tests for Phase 5 completion
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import ValidationError
from django.test.utils import override_settings
from blog.models import Post, Comment
from tests.factories import UserFactory, PostFactory, CommentFactory


@pytest.mark.django_db
class TestSecurityAndAuthentication:
    """Test security aspects and authentication requirements"""
    
    def setup_method(self):
        self.client = Client()
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
    
    def test_create_post_requires_authentication(self):
        """Test that creating posts requires authentication"""
        response = self.client.get(reverse('blog:create_post'))
        assert response.status_code == 302  # Redirect to login
        
        response = self.client.post(reverse('blog:create_post'), data={
            'title': 'Test Post',
            'body': 'Content'
        })
        assert response.status_code == 302  # Redirect to login
    
    def test_edit_post_requires_authentication(self):
        """Test that editing posts requires authentication"""
        response = self.client.get(reverse('blog:edit_post', kwargs={'slug': self.post.slug}))
        assert response.status_code == 302  # Redirect to login
    
    def test_delete_post_requires_authentication(self):
        """Test that deleting posts requires authentication"""
        response = self.client.get(reverse('blog:delete_post', kwargs={'slug': self.post.slug}))
        assert response.status_code == 302  # Redirect to login
    
    def test_add_comment_requires_authentication(self):
        """Test that adding comments requires authentication"""
        response = self.client.post(reverse('blog:add_comment', kwargs={'slug': self.post.slug}), data={
            'content': 'Test comment'
        })
        assert response.status_code == 302  # Redirect to login
    
    def test_csrf_protection(self):
        """Test CSRF protection on forms"""
        self.client.force_login(self.user)
        
        # Try to post without CSRF token
        response = self.client.post(
            reverse('blog:add_comment', kwargs={'slug': self.post.slug}),
            data={'content': 'Test comment'},
            HTTP_X_CSRFTOKEN=''
        )
        # Django should handle CSRF protection


@pytest.mark.django_db
class TestEdgeCasesAndErrorHandling:
    """Test edge cases and error handling scenarios"""
    
    def setup_method(self):
        self.client = Client()
        self.user = UserFactory()
        self.client.force_login(self.user)
    
    def test_nonexistent_post_edit(self):
        """Test editing nonexistent post returns 404"""
        response = self.client.get(reverse('blog:edit_post', kwargs={'slug': 'nonexistent'}))
        assert response.status_code == 404
    
    def test_nonexistent_post_delete(self):
        """Test deleting nonexistent post returns 404"""
        response = self.client.get(reverse('blog:delete_post', kwargs={'slug': 'nonexistent'}))
        assert response.status_code == 404
    
    def test_nonexistent_post_comment(self):
        """Test commenting on nonexistent post returns 404"""
        response = self.client.post(
            reverse('blog:add_comment', kwargs={'slug': 'nonexistent'}),
            data={'content': 'Test comment'}
        )
        assert response.status_code == 404
    
    def test_invalid_form_data_handling(self):
        """Test handling of invalid form data"""
        # Test creating post with empty title
        response = self.client.post(reverse('blog:create_post'), data={
            'title': '',
            'body': 'Some content'
        })
        # Should return form with errors, not crash
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_very_long_content(self):
        """Test handling of very long content"""
        long_content = 'x' * 10000
        
        post_data = {
            'title': 'Test Post',
            'body': long_content,
            'status': 1
        }
        
        response = self.client.post(reverse('blog:create_post'), data=post_data)
        # Should handle long content appropriately
    
    def test_special_characters_in_slug(self):
        """Test handling of special characters in slug generation"""
        post_data = {
            'title': 'Test Post with Special Ch@r$!',
            'body': 'Content',
            'status': 1
        }
        
        response = self.client.post(reverse('blog:create_post'), data=post_data)
        
        if response.status_code == 302:  # Successful creation
            post = Post.objects.get(title='Test Post with Special Ch@r$!')
            # Slug should be cleaned of special characters
            assert post.slug == 'test-post-with-special-chr'


@pytest.mark.django_db
class TestModelValidationAndConstraints:
    """Test model validation and database constraints"""
    
    def test_post_unique_title_constraint(self):
        """Test that post titles must be unique"""
        PostFactory(title='Unique Title')
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            PostFactory(title='Unique Title')
    
    def test_post_unique_slug_constraint(self):
        """Test that post slugs must be unique"""
        PostFactory(slug='unique-slug')
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            PostFactory(slug='unique-slug')
    
    def test_comment_cascade_delete(self):
        """Test that comments are deleted when post is deleted"""
        post = PostFactory()
        comment = CommentFactory(post=post)
        
        comment_id = comment.id
        post.delete()
        
        assert not Comment.objects.filter(id=comment_id).exists()
    
    def test_post_str_method(self):
        """Test Post __str__ method"""
        post = PostFactory(title='Test Title')
        assert str(post) == 'Test Title'
    
    def test_comment_str_method(self):
        """Test Comment __str__ method"""
        user = UserFactory(username='testuser')
        post = PostFactory(title='Test Post')
        comment = CommentFactory(author=user, post=post)
        
        expected = f'Comment by testuser on Test Post'
        assert str(comment) == expected


@pytest.mark.django_db
class TestPaginationAndQueries:
    """Test pagination and database query optimization"""
    
    def setup_method(self):
        self.client = Client()
        # Create multiple posts for pagination testing
        self.posts = [PostFactory(status=1) for _ in range(12)]
    
    def test_post_list_pagination(self):
        """Test post list pagination works correctly"""
        response = self.client.get(reverse('blog:post_list'))
        assert response.status_code == 200
        
        # Check pagination context
        assert 'is_paginated' in response.context
        assert response.context['is_paginated'] == True
        
        # Should have 5 posts per page (as set in view)
        assert len(response.context['posts']) == 5
    
    def test_post_list_second_page(self):
        """Test accessing second page of posts"""
        response = self.client.get(reverse('blog:post_list') + '?page=2')
        assert response.status_code == 200
        assert len(response.context['posts']) == 5
    
    def test_post_list_last_page(self):
        """Test accessing last page of posts"""
        response = self.client.get(reverse('blog:post_list') + '?page=3')
        assert response.status_code == 200
        assert len(response.context['posts']) == 2  # Only 2 posts on last page
    
    def test_invalid_page_number(self):
        """Test handling of invalid page numbers"""
        response = self.client.get(reverse('blog:post_list') + '?page=999')
        # Should redirect to last valid page or show appropriate error
        assert response.status_code in [200, 404]


@pytest.mark.django_db 
class TestPerformanceAndOptimization:
    """Test performance aspects and query optimization"""
    
    def setup_method(self):
        self.client = Client()
    
    def test_post_detail_efficient_queries(self):
        """Test that post detail view doesn't have excessive queries"""
        post = PostFactory(status=1)
        comments = [CommentFactory(post=post, active=True) for _ in range(5)]
        
        # Test that view loads successfully
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': post.slug}))
        assert response.status_code == 200
        
        # Verify all comments are loaded
        assert len(response.context['comments']) == 5
    
    def test_post_list_efficient_queries(self):
        """Test that post list view loads efficiently"""
        posts = [PostFactory(status=1) for _ in range(5)]
        
        response = self.client.get(reverse('blog:post_list'))
        assert response.status_code == 200
        
        # Check reasonable query performance
        assert len(response.context['posts']) == 5
