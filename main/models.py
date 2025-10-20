from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # slug = models.SlugField(unique=True, blank=True)


    def __str__(self):
        return self.title

    def get_summary(self):
        return self.content[:50]
