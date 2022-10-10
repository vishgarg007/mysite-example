# blog/models.py
from django.conf import settings
from django.db import models

class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # No duplicates!
        null=False,
    )
    slug = models.SlugField(
        unique=True,
        null=False,
    )
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',
        null=False,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )
    content = models.TextField()
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published'
    )
    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save

    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
