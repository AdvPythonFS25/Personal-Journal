from django.test import TestCase
from django.contrib.auth.models import User
from entries.models import Entry


class EntryModelTest(TestCase):
    def test_entry_creation(self):
        
        # Create a test user (with username, email and password)
        user = User.objects.create_user('tester', 't@t.com', 'pass')
        
        # Log in the test client using the created user
        self.client.force_login(user)
        
        # Simulate submitting a POST request to the entry creation view,
        # passes in form data for 'title' and 'content'
        response = self.client.post('/accounts/create/', {
            'title': 'Test Entry',
            'content': 'Testing content.',
        })
        
        # Assert that exactly one Entry object now exists in the database
        self.assertEqual(Entry.objects.count(), 1)



