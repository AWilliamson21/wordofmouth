import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from gdstorage.storage import GoogleDriveStorage

gd_storage = GoogleDriveStorage()


class Recipe(models.Model):
    objects = None
    title = models.CharField(max_length = 200)
    ingredients = models.TextField(default="")
    recipe = models.TextField(default="")
    '''
    Title: Django - how to make ImageField/FileField optional
    Author: orthodoxpirate
    Date: 10/15/2014
    Code version: Django v4.0
    URL: https://stackoverflow.com/questions/2677637/django-how-to-make-imagefield-filefield-optional
    Software License: BSD
    '''
    '''
    Title: Model Field Reference
    Author: Django Software Foundation and individual contributors
    Date: 2005-2022
    Code Version: Django v4.0
    URL: https://docs.djangoproject.com/en/4.0/ref/models/fields/
    Software License: BSD
    '''
    photo = models.ImageField(storage=gd_storage, blank=True)
    likes = models.IntegerField(default=0)
    author = models.CharField(max_length=200, default="anonymous")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Fork(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='forks')
    title = models.CharField(max_length=200)
    ingredients = models.TextField(default="")
    instructions = models.TextField(default="")
    photo = models.ImageField(storage=gd_storage, blank=True)
    author = models.CharField(max_length=200, default="anonymous")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class MultiRecipe(models.Model):
    title = models.CharField(max_length = 200)
    # stores text descriptions to be added to the article
    '''
    Title: Model Field Reference
    Author: Django Software Foundation and individual contributors
    Date: 2005-2022
    Code Version: Django v4.0
    URL: https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.JSONField
    Software License: BSD
    '''
    descriptions = models.JSONField(default=list)
    # stores pk keys connected to the Recipe objects involved in the article
    recipes = models.JSONField(default=list)
    author = models.CharField(max_length=200, default="anonymous")
    '''
    Title: Model Field Reference
    Author: Django Software Foundation and individual contributors
    Date: 2005-2022
    Code Version: Django v4.0
    URL: https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.DateField.auto_now_add
    Software License: BSD
    '''
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    body = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time_posted']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class ForkComment(models.Model):
    recipe = models.ForeignKey(Fork, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    body = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time_posted']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
