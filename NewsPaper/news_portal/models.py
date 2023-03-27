from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_posts_rating = self.post_set.all().aggregate(Sum('post_rating'))['post_rating__sum'] * 3
        sum_comments = self.user.comment_set.all().aggregate(Sum('comment_rating'))['comment_rating__sum']
        sum_comments_post = self.post_set.all().aggregate(Sum('comment__comment_rating'))[
            'comment__comment_rating__sum']
        self.rating = sum_posts_rating + sum_comments + sum_comments_post
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    post = models.ManyToManyField('Post', through='PostCategory', related_name='post')


class Post(models.Model):
    TYPE = [('news', 'Новости'),
            ('article', 'Статья')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=TYPE, default='news')
    post_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory', related_name='category')
    header = models.CharField(max_length=128)
    text = models.TextField(default='Здесь может быть текст вашей новости или статьи!')
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
