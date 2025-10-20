from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from main.forms import PostForm
from main.models import Post


class IndexViewTest(TestCase):
    """
    Index view အတွက် unit test
    - GET request → HTTP 200, template, context စမ်းသပ်
    - GET method restriction → POST လုပ်ရင် 405 စမ်းသပ်
    """

    def setUp(self):
        """Test client ဖန်တီးပြီး test data create"""
        self.client = Client()
        self.post1 = Post.objects.create(title="Post 1", content="အကြောင်းအရာ 1")
        self.post2 = Post.objects.create(title="Post 2", content="အကြောင်းအရာ 2")

    def test_get_status_code(self):
        """GET request → HTTP 200 OK စမ်းသပ်"""
        response = self.client.get(reverse('website:index'))
        self.assertEqual(response.status_code, 200)

    def test_template_and_context(self):
        """Correct template အသုံးပြုမှုနှင့် context မှာ Post objects ပါမယ် စမ်းသပ်"""
        response = self.client.get(reverse('website:index'))
        self.assertTemplateUsed(response, 'index.html')
        items = response.context['items']
        self.assertEqual(list(items), [self.post1, self.post2])

    def test_post_method_not_allowed(self):
        """POST request → 405 Method Not Allowed စမ်းသပ်"""
        response = self.client.post(reverse('website:index'))
        self.assertEqual(response.status_code, 405)


class GetDetailViewTest(TestCase):
    """
    get_detail view အတွက် unit test
    - Object ရှိ/မရှိ branch
    - GET method restriction
    - Template rendering, context, redirect, message စမ်းသပ်
    """

    def setUp(self):
        """Test client နှင့် valid Post object create"""
        self.client = Client()
        self.post = Post.objects.create(title="Test Post", content="Sample content")

    def test_get_detail_object_exists(self):
        """Valid PK → detail.html render, context correct, HTTP 200 OK"""
        url = reverse('website:get-detail', args=[self.post.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual(response.context['item'], self.post)

    def test_get_detail_object_does_not_exist(self):
        """Invalid PK → redirect to index, error message"""
        invalid_pk = self.post.pk + 1
        url = reverse('website:get-detail', args=[invalid_pk])
        response = self.client.get(url, follow=True)

        self.assertRedirects(response, reverse('website:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Id not found" in str(m) for m in messages))

    def test_post_method_not_allowed(self):
        """POST request → 405 Method Not Allowed စမ်းသပ်"""
        url = reverse('website:get-detail', args=[self.post.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)


class CreatePostViewTest(TestCase):
    """
    create_post view အတွက် unit test
    - GET request → blank form render
    - POST valid → DB save, success message, redirect
    - POST invalid → form errors, error message, same template render
    """

    def setUp(self):
        """Test client create"""
        self.client = Client()
        self.url = reverse('website:create-post')

    def test_get_request_renders_blank_form(self):
        """GET request → blank PostForm render"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_post.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_valid_data_creates_post(self):
        """POST valid data → Post object save, redirect, success message"""
        data = {'title': 'Test Post', 'content': 'Some test content'}
        response = self.client.post(self.url, data)

        self.assertRedirects(response, reverse('website:index'))
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'Some test content')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("successfully" in str(m) for m in messages))

    def test_post_invalid_data_shows_error(self):
        """POST invalid data → form errors, error message, same template render"""
        data = {'title': '', 'content': ''}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_post.html')
        form = response.context['form']
        self.assertTrue(form.errors)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("fail" in str(m) for m in messages))


class UpdatePostViewTest(TestCase):
    """
    update_post view အတွက် unit test
    - GET request → form instance render
    - POST valid → DB update, redirect, success message
    - POST invalid → form errors, error message
    - Invalid PK → redirect + error message
    """

    def setUp(self):
        """Test client နှင့် test Post object create"""
        self.client = Client()
        self.post = Post.objects.create(title="Original Title", content="Original content")
        self.url = reverse('website:update-post', args=[self.post.pk])
        self.invalid_url = reverse('website:update-post', args=[9999])  # မရှိတဲ့ PK

    def test_get_request_renders_form(self):
        """GET request → PostForm instance render"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_post.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], PostForm)

    def test_post_valid_updates_post(self):
        """POST valid data → Post object update, redirect, success message"""
        data = {'title': 'Updated Title', 'content': 'Updated content'}
        response = self.client.post(self.url, data)

        self.assertRedirects(response, reverse('website:index'))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.content, 'Updated content')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Update successfully" in str(m) for m in messages))

    def test_post_invalid_shows_error(self):
        """POST invalid data → form errors, error message, same template render"""
        data = {'title': '', 'content': ''}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_post.html')
        form = response.context['form']
        self.assertTrue(form.errors)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Update failed" in str(m) for m in messages))

    def test_update_nonexistent_post_redirects(self):
        """Invalid PK → redirect to index, error message"""
        response = self.client.get(self.invalid_url)
        self.assertRedirects(response, reverse('website:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Id not found" in str(m) for m in messages))
