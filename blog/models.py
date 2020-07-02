import markdown
from django.utils.html import strip_tags
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Post(models.Model):
    title = models.CharField(max_length=70, verbose_name='标题')
    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(
        verbose_name='创建时间', default=timezone.now)
    modified_time = models.DateTimeField(verbose_name='修改时间')
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='摘要')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='分类')
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='作者')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        if not self.excerpt:
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
