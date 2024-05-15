from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
import bleach
# from taggit.managers import TaggableManager

User = get_user_model()


class BlogPost(models.Model):
    STATUS_CHOICES = (
        (0, 'Draft'),
        (1, 'Published'),
        (2, 'Archived'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200, unique_for_date='publish', default='')
    content = models.TextField()
    content_short = models.CharField(max_length=300, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    # tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.content_short = bleach.clean(self.content, tags=[], strip=True)[
            :300]
        if self.status == 1:
            self.publish = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
