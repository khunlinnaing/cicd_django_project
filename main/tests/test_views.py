from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from main.views import INDEX_URL_NAME
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


class GetCreatePostViewTest(TestCase):
    """
    get_create_post view အတွက် unit test များ။
    - GET request မှာ HTTP 200 OK ဖြစ်ရမယ်။
    - မှန်ကန်တဲ့ template သုံးထားဖို့။
    - Context မှာ PostForm ပါဖို့ စမ်းသပ်။
    """

    def setUp(self):
        """Test client ပြင်ဆင်မှု"""
        self.client = Client()
        self.url = reverse("website:get-create-post")  # သင့် urls.py ထဲက name နဲ့ ကိုက်ရမယ်။

    def test_get_request_status_code(self):
        """GET request → HTTP 200 OK ဖြစ်ရမယ်။"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_request_uses_correct_template(self):
        """မှန်ကန်တဲ့ template ကို အသုံးပြုထားမလား စမ်းသပ်"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "create_post.html")

    def test_context_contains_form_and_action(self):
        """Context မှာ form နဲ့ action key ၂ ခုပါရမယ်"""
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIn("action", response.context)
        self.assertIsInstance(response.context["form"], PostForm)


class PostCreatePostViewTest(TestCase):
    """
    post_create_post view အတွက် unit test များ။
    - POST valid data → DB save + redirect + success message
    - POST invalid data → template render + error message
    - GET method → 405 (method not allowed)
    """

    def setUp(self):
        """Test client ပြင်ဆင်မှု"""
        self.client = Client()
        self.url = reverse("website:post-create-post")

    def test_post_valid_data_creates_post(self):
        """POST valid data → DB save + success message + redirect"""
        data = {
            "title": "New Post",
            "content": "This is a new post."
        }
        response = self.client.post(self.url, data)

        # Redirect စစ်
        from main.views import INDEX_URL_NAME
        self.assertRedirects(response, reverse(INDEX_URL_NAME))

        # DB မှာ post တစ်ခုဖြစ်သင့်
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.title, "New Post")

        # Success message ပါသင့်
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("successfully" in str(m) for m in messages))

    def test_post_invalid_data_renders_form(self):
        """POST invalid data → Form errors + Error message + same template"""
        data = {
            "title": "",  # Required field blank
            "content": ""
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_post.html")

        form = response.context["form"]
        self.assertTrue(form.errors)  # Form invalid ဖြစ်ရမယ်။

        # Error message ပါသင့်
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("fail" in str(m) for m in messages))

    def test_get_request_not_allowed(self):
        """GET request → 405 Method Not Allowed ဖြစ်ရမယ်။"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)


class GetUpdatePostViewTest(TestCase):
    """
    get_update_post view အတွက် unit test များ။
    - GET request မှာ HTTP 200 OK ဖြစ်ရမယ်။
    - Template မှန်မမှန်စစ်ရမယ်။
    - Context data မှာ form နှင့် action ပါ/မပါ စစ်ခြင်း။
    - Post မရှိတဲ့အခါ redirect ဖြစ်ဖို့စစ်ခြင်း။
    """

    def setUp(self):
        """Test client ပြင်ဆင်ပြီး sample post တစ်ခုဖန်တီး"""
        self.client = Client()
        self.post = Post.objects.create(title="Old Title", content="Old content")
        self.url = reverse("website:get-update-post", args=[self.post.pk])

    def test_get_update_post_status_code(self):
        """GET request → HTTP 200 OK ဖြစ်ရမယ်။"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_update_post_uses_correct_template(self):
        """မှန်ကန်တဲ့ template ကို render လုပ်ထားဖို့ စစ်ခြင်း။"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "create_post.html")

    def test_context_contains_form_and_action(self):
        """Context data ထဲမှာ form နဲ့ action key တွေပါ/မပါ စစ်ခြင်း။"""
        response = self.client.get(self.url)
        self.assertIn("form", response.context)
        self.assertIn("action", response.context)
        self.assertIsInstance(response.context["form"], PostForm)

    def test_get_update_post_not_found_redirects(self):
        """မရှိတဲ့ Post ID → redirect + error message ဖြစ်ရမယ်။"""
        url = reverse("website:get-update-post", args=[999])  # မရှိတဲ့ ID
        response = self.client.get(url)
        self.assertRedirects(response, reverse(INDEX_URL_NAME))

        # message check
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Id not found" in str(m) for m in messages))


class PostUpdatePostViewTest(TestCase):
    """
    post_update_post view အတွက် unit test များ။
    - POST valid data → DB update + redirect + success message
    - POST invalid data → render same form + error message
    - Post မရှိရင် redirect + message
    - GET method → 405 (method not allowed)
    """

    def setUp(self):
        """Test client ပြင်ဆင်ပြီး sample post တစ်ခုဖန်တီး"""
        self.client = Client()
        self.post = Post.objects.create(title="Old Title", content="Old content")
        self.url = reverse("website:post-update-post", args=[self.post.pk])

    def test_post_valid_data_updates_post(self):
        """POST valid data → Update success + Redirect + Success message"""
        data = {
            "title": "Updated Title",
            "content": "Updated content"
        }
        response = self.client.post(self.url, data)

        # Redirect check
        self.assertRedirects(response, reverse(INDEX_URL_NAME))

        # Database update check
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")
        self.assertEqual(self.post.content, "Updated content")

        # Success message check
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Update successfully" in str(m) for m in messages))

    def test_post_invalid_data_shows_form(self):
        """POST invalid data → form error + error message + render same template"""
        data = {
            "title": "",  # required field blank
            "content": ""
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_post.html")

        form = response.context["form"]
        self.assertTrue(form.errors)  # Invalid form ဖြစ်ရမယ်။

        # Error message check
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Update failed" in str(m) for m in messages))

    def test_post_not_found_redirects(self):
        """POST မရှိတဲ့ ID → redirect + error message ဖြစ်ရမယ်။"""
        url = reverse("website:post-update-post", args=[999])  # မရှိတဲ့ ID
        data = {"title": "Anything", "content": "Text"}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse(INDEX_URL_NAME))

        # message check
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Id not found" in str(m) for m in messages))

    def test_get_request_not_allowed(self):
        """GET request → 405 Method Not Allowed ဖြစ်ရမယ်။"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

