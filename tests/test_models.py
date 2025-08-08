import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from blog.models import Post, Comment
from tests.factories import UserFactory, PostFactory, CommentFactory, DraftPostFactory


@pytest.mark.django_db
class TestPostModel:
    """Test cases for Post model"""
    
    def test_post_creation(self):
        """Test basic post creation"""
        user = UserFactory()
        post = PostFactory(author=user)
        
        assert post.title
        assert post.slug
        assert post.body
        assert post.author == user
        assert post.status == 1  # Published
        assert post.created_at
        assert post.updated_at
    
    def test_post_str_method(self):
        """Test __str__ method returns title"""
        post = PostFactory(title="Test Post Title")
        assert str(post) == "Test Post Title"
    
    def test_post_get_absolute_url(self):
        """Test get_absolute_url method"""
        post = PostFactory(slug="test-post")
        expected_url = reverse('blog:post_detail', kwargs={'slug': 'test-post'})
        assert post.get_absolute_url() == expected_url
    
    def test_post_ordering(self):
        """Test posts are ordered by created_at descending"""
        post1 = PostFactory()
        post2 = PostFactory()
        
        posts = Post.objects.all()
        assert posts[0].created_at >= posts[1].created_at
    
    def test_unique_title_constraint(self):
        """Test title uniqueness constraint"""
        PostFactory(title="Unique Title")
        
        with pytest.raises(Exception):  # IntegrityError
            PostFactory(title="Unique Title")
    
    def test_unique_slug_constraint(self):
        """Test slug uniqueness constraint"""
        PostFactory(slug="unique-slug")
        
        with pytest.raises(Exception):  # IntegrityError
            PostFactory(slug="unique-slug")
    
    def test_draft_post(self):
        """Test draft post creation"""
        draft = DraftPostFactory()
        assert draft.status == 0
    
    def test_published_post(self):
        """Test published post creation"""
        post = PostFactory()
        assert post.status == 1


@pytest.mark.django_db
class TestCommentModel:
    """Test cases for Comment model"""
    
    def test_comment_creation(self):
        """Test basic comment creation"""
        post = PostFactory()
        user = UserFactory()
        comment = CommentFactory(post=post, author=user)
        
        assert comment.post == post
        assert comment.author == user
        assert comment.content
        assert comment.created_at
        assert comment.active is True
    
    def test_comment_str_method(self):
        """Test __str__ method"""
        user = UserFactory(username="testuser")
        post = PostFactory(title="Test Post")
        comment = CommentFactory(author=user, post=post)
        
        expected = f"Comment by testuser on Test Post"
        assert str(comment) == expected
    
    def test_comment_related_name(self):
        """Test comments can be accessed via post.comments"""
        post = PostFactory()
        comment1 = CommentFactory(post=post)
        comment2 = CommentFactory(post=post)
        
        assert post.comments.count() == 2
        assert comment1 in post.comments.all()
        assert comment2 in post.comments.all()
    
    def test_inactive_comment(self):
        """Test inactive comment creation"""
        comment = CommentFactory(active=False)
        assert comment.active is False
    
    def test_comment_cascade_delete(self):
        """Test comment is deleted when post is deleted"""
        post = PostFactory()
        comment = CommentFactory(post=post)
        comment_id = comment.id
        
        post.delete()
        
        assert not Comment.objects.filter(id=comment_id).exists()
