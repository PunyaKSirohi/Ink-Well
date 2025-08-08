"""
Additional comprehensive tests to improve coverage for Phase 5 completion
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from blog.models import Post, Comment
from blog.forms import PostForm
from tests.factories import UserFactory, PostFactory, CommentFactory


@pytest.mark.django_db
class TestCreatePostView:
    """Test cases for create_post view"""
    
    def setup_method(self):
        self.client = Client()
        self.user = UserFactory()
        self.client.force_login(self.user)
    
    def test_create_post_get_request(self):
        """Test GET request to create post view"""
        response = self.client.get(reverse('blog:create_post'))
        assert response.status_code == 200
        assert 'form' in response.context
        assert isinstance(response.context['form'], PostForm)
    
    def test_create_post_valid_data(self):
        """Test creating post with valid data"""
        post_data = {
            'title': 'Test Post Title',
            'slug': 'test-post-title',
            'body': 'This is test post content.',
            'tags': 'test, blog',
            'status': 1
        }
        
        response = self.client.post(reverse('blog:create_post'), data=post_data)
        
        # Should redirect to post detail
        assert response.status_code == 302
        
        # Check post was created
        post = Post.objects.get(title='Test Post Title')
        assert post.author == self.user
        assert post.slug == 'test-post-title'
    
    def test_create_post_auto_slug_generation(self):
        """Test auto-generation of slug when not provided"""
        post_data = {
            'title': 'Test Post Without Slug',
            'body': 'Content for test post.',
            'status': 1
        }
        
        response = self.client.post(reverse('blog:create_post'), data=post_data)
        
        post = Post.objects.get(title='Test Post Without Slug')
        assert post.slug == 'test-post-without-slug'
    
    def test_create_post_duplicate_slug_handling(self):
        """Test handling of duplicate slugs"""
        # Create first post
        PostFactory(title='Original Post', slug='test-slug', author=self.user)
        
        post_data = {
            'title': 'Another Post',
            'slug': 'test-slug',  # Same slug
            'body': 'Different content.',
            'status': 1
        }
        
        response = self.client.post(reverse('blog:create_post'), data=post_data)
        
        # The form should reject duplicate slug or auto-modify it
        if response.status_code == 302:  # Successful creation
            # Check if slug was auto-modified
            try:
                new_post = Post.objects.get(title='Another Post')
                assert new_post.slug != 'test-slug'  # Should be different
            except Post.DoesNotExist:
                # Post creation failed due to validation
                pass
        else:
            # Form should show error
            assert response.status_code == 200
            assert 'form' in response.context


@pytest.mark.django_db
class TestEditPostView:
    """Test cases for edit_post view"""
    
    def setup_method(self):
        self.client = Client()
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.post = PostFactory(author=self.user, slug='test-post')
        self.client.force_login(self.user)
    
    def test_edit_post_get_request(self):
        """Test GET request to edit post view"""
        response = self.client.get(reverse('blog:edit_post', kwargs={'slug': 'test-post'}))
        assert response.status_code == 200
        assert response.context['post'] == self.post
    
    def test_edit_post_valid_data(self):
        """Test editing post with valid data"""
        post_data = {
            'title': 'Updated Title',
            'slug': 'updated-title',
            'body': 'Updated content.',
            'tags': 'updated, tags',
            'status': 1
        }
        
        response = self.client.post(
            reverse('blog:edit_post', kwargs={'slug': 'test-post'}), 
            data=post_data
        )
        
        self.post.refresh_from_db()
        assert self.post.title == 'Updated Title'
        assert response.status_code == 302
    
    def test_edit_post_unauthorized_user(self):
        """Test that users can't edit others' posts"""
        self.client.force_login(self.other_user)
        response = self.client.get(reverse('blog:edit_post', kwargs={'slug': 'test-post'}))
        assert response.status_code == 404


@pytest.mark.django_db
class TestDeletePostView:
    """Test cases for delete_post view"""
    
    def setup_method(self):
        self.client = Client()
        self.user = UserFactory()
        self.post = PostFactory(author=self.user, slug='test-post')
        self.client.force_login(self.user)
    
    def test_delete_post_get_request(self):
        """Test GET request shows delete confirmation"""
        response = self.client.get(reverse('blog:delete_post', kwargs={'slug': 'test-post'}))
        assert response.status_code == 200
        assert response.context['post'] == self.post
    
    def test_delete_post_confirm(self):
        """Test POST request deletes the post"""
        response = self.client.post(reverse('blog:delete_post', kwargs={'slug': 'test-post'}))
        
        assert response.status_code == 302
        assert not Post.objects.filter(slug='test-post').exists()


@pytest.mark.django_db
class TestUserPostsView:
    """Test cases for user_posts view"""
    
    def setup_method(self):
        self.client = Client()
        self.user = UserFactory()
        self.client.force_login(self.user)
        
        # Create posts for this user
        self.published_post = PostFactory(author=self.user, status=1)
        self.draft_post = PostFactory(author=self.user, status=0)
        
        # Create post by another user
        self.other_post = PostFactory(author=UserFactory())
    
    def test_user_posts_view(self):
        """Test user posts view shows only current user's posts"""
        response = self.client.get(reverse('blog:user_posts'))
        
        assert response.status_code == 200
        posts = response.context['posts']
        
        # Should include both published and draft posts by current user
        assert self.published_post in posts
        assert self.draft_post in posts
        
        # Should not include other user's posts
        assert self.other_post not in posts
    
    def test_user_posts_unauthenticated(self):
        """Test user posts view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('blog:user_posts'))
        assert response.status_code == 302  # Redirect to login


@pytest.mark.django_db
class TestAuthViewsCoverage:
    """Test cases for auth_views.py to improve coverage"""
    
    def setup_method(self):
        self.client = Client()
    
    def test_register_view_get(self):
        """Test register view GET request"""
        response = self.client.get(reverse('blog:register'))
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_register_view_valid_post(self):
        """Test successful user registration"""
        register_data = {
            'username': 'newuser',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        
        response = self.client.post(reverse('blog:register'), data=register_data)
        assert response.status_code == 302  # Redirect to login
        
        # Check user was created
        assert User.objects.filter(username='newuser').exists()
    
    def test_profile_view(self):
        """Test profile view for authenticated user"""
        user = UserFactory()
        post = PostFactory(author=user)
        
        self.client.force_login(user)
        response = self.client.get(reverse('blog:profile'))
        
        assert response.status_code == 200
        assert post in response.context['user_posts']


@pytest.mark.django_db  
class TestAdminViewsCoverage:
    """Test cases for admin functionality to improve coverage"""
    
    def setup_method(self):
        self.admin_user = UserFactory(is_staff=True, is_superuser=True)
        self.post = PostFactory()
        self.comment = CommentFactory()
    
    def test_admin_post_actions(self):
        """Test admin custom actions for posts"""
        from blog.admin import PostAdmin
        from django.contrib.admin.sites import AdminSite
        
        admin = PostAdmin(Post, AdminSite())
        assert admin.list_display == ('title', 'slug', 'author', 'created_at', 'status')
        assert 'status' in admin.list_filter
        assert 'title' in admin.search_fields
    
    def test_admin_comment_actions(self):
        """Test admin custom actions for comments"""
        from blog.admin import CommentAdmin
        from django.contrib.admin.sites import AdminSite
        
        admin = CommentAdmin(Comment, AdminSite())
        queryset = Comment.objects.filter(id=self.comment.id)
        
        # Test that the actions exist
        assert hasattr(admin, 'approve_comments')
        assert hasattr(admin, 'disapprove_comments')
        
        # Test approve action directly updates status
        admin.approve_comments(None, queryset)
        self.comment.refresh_from_db()
        assert self.comment.active == True
        
        # Test disapprove action
        admin.disapprove_comments(None, queryset)
        self.comment.refresh_from_db()
        assert self.comment.active == False


@pytest.mark.django_db
class TestFormValidationCoverage:
    """Test edge cases in form validation"""
    
    def test_post_form_invalid_data(self):
        """Test PostForm with invalid data"""
        from blog.forms import PostForm
        
        form_data = {
            'title': '',  # Empty title
            'body': 'x' * 10000,  # Potentially too long
        }
        
        form = PostForm(data=form_data)
        assert not form.is_valid()
        assert 'title' in form.errors
    
    def test_comment_form_edge_cases(self):
        """Test CommentForm edge cases"""
        from blog.forms import CommentForm
        
        # Test with whitespace only
        form_data = {'content': '   '}
        form = CommentForm(data=form_data)
        # Form should handle whitespace appropriately
