from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import re


class UserManager(models.Manager):
    def user_validator(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data['first_name']) <= 2:
            errors['first_name'] = 'Please enter valid first name'
        if len(data['last_name']) <= 2:
            errors['lsat_name'] = 'Please enter valid last name.'

        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Invalid email address!"
        try:
            User.objects.get(email=data['email'])
            errors['email'] = 'Email already in use.'
        except:
            pass

        if len(data['password']) <= 7:
            errors['password'] = 'Please enter a password 8 characters or more'
        if data['password'] != data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    confirm_password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class JobManager(models.Manager):
    def basic_validator(self, data):
        errors = {}
        if len(data['title']) <= 2:
            errors['title'] = "Please enter a job title 3 characters or more."
        if len(data['desc']) <= 2:
            errors['desc'] = "Please enter a description 3 characters or more."
        if len(data['location']) <= 2:
            errors['location'] = "Please enter a valid location for job posting. (City and State)"
        return errors


class Job(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    location = models.CharField(max_length=45)
    user = models.ForeignKey(User, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()
