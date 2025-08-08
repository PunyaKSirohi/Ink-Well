import pytest
from django.test import TestCase
from blog.forms import CommentForm
from tests.factories import UserFactory, PostFactory


@pytest.mark.django_db
class TestCommentForm:
    """Test cases for CommentForm"""
    
    def test_comment_form_valid_data(self):
        """Test comment form with valid data"""
        form_data = {
            'content': 'This is a valid comment content.'
        }
        
        form = CommentForm(data=form_data)
        assert form.is_valid()
    
    def test_comment_form_empty_content(self):
        """Test comment form with empty content"""
        form_data = {
            'content': ''
        }
        
        form = CommentForm(data=form_data)
        assert not form.is_valid()
        assert 'content' in form.errors
    
    def test_comment_form_content_too_long(self):
        """Test comment form with content exceeding max length"""
        form_data = {
            'content': 'x' * 1001  # Assuming max_length is 1000
        }
        
        form = CommentForm(data=form_data)
        # This test depends on your Comment model's max_length for content
        # Adjust accordingly
    
    def test_comment_form_save(self):
        """Test comment form save method"""
        user = UserFactory()
        post = PostFactory()
        
        form_data = {
            'content': 'Test comment content'
        }
        
        form = CommentForm(data=form_data)
        assert form.is_valid()
        
        comment = form.save(commit=False)
        comment.author = user
        comment.post = post
        comment.save()
        
        assert comment.content == 'Test comment content'
        assert comment.author == user
        assert comment.post == post
        assert comment.active is True  # Default value
    
    def test_comment_form_widget_attrs(self):
        """Test comment form widget attributes"""
        form = CommentForm()
        
        # Check if the content field has the right widget attributes
        content_widget = form.fields['content'].widget
        assert 'class' in content_widget.attrs
        assert 'placeholder' in content_widget.attrs
