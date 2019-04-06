from django.db import models
from django.utils import timezone
from django.urls import reverse
#from django.contrib import auth

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length = 30)
    text = models.TextField()
    create_date = models.DateField(default=timezone.now)
    publish_date = models.DateField(blank=True, null=True)

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.pk})

    def approved_comments(self):
        return self.comments.filter(approved_comment = True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=30)
    text = models.TextField()
    create_date = models.DateField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('posts')
