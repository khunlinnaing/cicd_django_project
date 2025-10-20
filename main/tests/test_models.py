from django.test import TestCase
from main.models import Post

class PostModelTest(TestCase):
    """
    Post Model အတွက် စမ်းသပ်မှုများ။
    __str__() နှင့် get_summary() method အပြည့်အဝစမ်းသပ်ရန်။
    """

    def test_post_creation(self):
        """Post object ကို create လုပ်နိုင်ပြီး field values မှန်ကြောင်း စမ်းသပ်"""
        post = Post.objects.create(
            title="Hello World",
            content="ဒီက unit test အတွက် စမ်းသပ် content ဖြစ်ပါတယ်။"
        )
        self.assertEqual(post.title, "Hello World")
        self.assertEqual(post.content, "ဒီက unit test အတွက် စမ်းသပ် content ဖြစ်ပါတယ်။")

    def test_str_method_returns_title(self):
        """__str__() method က Post ရဲ့ title ကို return လုပ်မလား စမ်းသပ်"""
        post = Post.objects.create(title="My Title", content="အကြောင်းအရာ")
        self.assertEqual(str(post), "My Title")

    def test_get_summary_returns_first_50_chars(self):
        """get_summary() က content အနည်းဆုံး 50 characters return လုပ်မလား စမ်းသပ်"""
        content = "က" * 100  # 100 characters ရှိ content
        post = Post.objects.create(title="Title", content=content)
        self.assertEqual(post.get_summary(), content[:50])

    def test_get_summary_with_short_content(self):
        """content 50 character ထက်နည်းရင် get_summary() က content အပြည့် return လုပ်မလား စမ်းသပ်"""
        short_content = "တိုတို content"
        post = Post.objects.create(title="Short Post", content=short_content)
        self.assertEqual(post.get_summary(), short_content)
