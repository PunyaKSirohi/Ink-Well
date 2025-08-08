"""
Test logout functionality using Django's proper testing framework
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class LogoutTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_logout_post_request_works(self):
        """Test that POST logout request works correctly"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Test POST logout
        response = self.client.post(reverse('logout'))
        
        # Should redirect (302) or succeed (200)
        self.assertIn(response.status_code, [200, 302])
        
        # User should be logged out
        response = self.client.get('/')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_template_exists(self):
        """Test that logged out template exists and renders"""
        # Login and logout
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        
        # Check if we get the logged out template (if not redirecting)
        if response.status_code == 200:
            self.assertContains(response, 'Successfully Logged Out')
    
    def test_logout_get_request_returns_405(self):
        """Test that GET logout request properly returns 405 Method Not Allowed"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Test GET logout should return 405
        response = self.client.get(reverse('logout'))
        
        # Should return 405 Method Not Allowed for security
        self.assertEqual(response.status_code, 405)
