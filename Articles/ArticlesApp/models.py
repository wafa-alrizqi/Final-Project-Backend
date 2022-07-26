from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    """This class for Category attributes """

    class CategoryTopic(models.TextChoices):
        BUSINESS = 'business'
        HEALTH = 'health'
        SPORT = 'sport'
        TECHNOLOGY = 'technology'
        ECONOMY = 'economy'
        ENTERTAINMENT = 'entertainment'
        FOOD_DRINK = 'Food and drink'

    name = models.CharField(choices=CategoryTopic.choices, max_length=30)
    image = models.URLField()

    def __str__(self):
        return self.name


class Article(models.Model):
    """ This class is for Articles attributes"""

    title = models.CharField(max_length=128)
    image = models.URLField()
    content = models.CharField(max_length=5000)
    summary = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    reference = models.URLField()
    likes = models.IntegerField(default=0)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """ This class for Comment attributes """

    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Bookmark(models.Model):
    """ This class for BookMarks attributes """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class FavouiteCatgory(models.Model):
    """ This class for Favouite Catgory attributes """

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


