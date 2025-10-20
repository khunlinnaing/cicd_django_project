from django.test import TestCase
from main.forms import PostForm
from main.models import Post

class PostFormTest(TestCase):
    """
    PostForm အတွက် unit test
    - valid input → form valid, save creates object
    - invalid input → form invalid
    """

    def test_form_valid_data(self):
        """Valid data → form.is_valid() True, save works"""
        data = {
            'title': 'Test Post',
            'content': 'Some test content'
        }
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())
        post = form.save()
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.title, 'Test Post')

    def test_form_invalid_blank_fields(self):
        """Blank fields → form.is_valid() False"""
        data = {
            'title': '',
            'content': ''
        }
        form = PostForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('content', form.errors)
