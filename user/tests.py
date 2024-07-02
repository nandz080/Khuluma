from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

class UserSignupTest(TestCase):
    def test_signup_page(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_signup(self):
        User = get_user_model()
        response = self.client.post(reverse('account_signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'AComplexPassword123!',
            'password2': 'AComplexPassword123!'
        })
        if response.status_code != 302:
            print(response.content)  # Print the response content for debugging
        self.assertEqual(response.status_code, 302)  # Redirects after signup
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
