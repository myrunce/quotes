# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator 
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def validation(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Name needs to be at least 2 characters long!"
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = 'Not a valid email!'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long!'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Passwords do not match!'
        return errors

class QuoteManager(models.Manager):
    def validation(self, postData):
        errors = {}
        if len(postData['quoted_by']) < 3:
            errors['quoted_by'] = 'Quoted By must be longer than 3 characters!'
        if len(postData['quote']) < 10:
            errors['quote'] = "Quote must be longer than 10 characters!"
        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField(auto_now=False, auto_now_add=False) 
    objects = UserManager()

class Quote(models.Model):
    quoted_by = models.CharField(max_length = 255)
    desc = models.TextField()
    user = models.ForeignKey(User, related_name='quotes')
    objects = QuoteManager()

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites_user')
    quote = models.ForeignKey(Quote, related_name='favorites_quote')