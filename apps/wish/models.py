from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
import bcrypt
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # CHECKING IF FNAME AND LNAME ARE AT LEAST 2 CHARACTERS
        if len(postData['fname'])<2: 
            errors['fname'] = "First Name should be at least 2 characters."
        if len(postData['lname'])<2: 
            errors['lname'] = "Last Name should be at least 2 characters."
        # CHECKING PASSWORD TO BE 8 CHARACTERS, A NUMBER, CAPITAL, LOWERCASE, AND MATCH
        if len(postData['password'])<8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['checkpassword']:
            errors['nomatch'] = "Passwords must match."
        if not re.match('.*[0-9]', postData['password']):
            errors['pwnumber'] = "Your password must contain a number"
        if not re.match('.*[A-Z]', postData['password']):
            errors['pwupper'] = "Your password must contain at least 1 upper case character."
        if not re.match('.*[a-z]', postData['password']):
            errors['pwlower'] = "Your password must contain at least 1 lower case character." 
        # CHECKING EMAIL VALID FORMAT AND IN DATABASE
        if not EMAIL_REGEX.match(postData['email']):
            errors['format'] = "Invalid email address."
        if len(User.objects.filter(email=postData['email']))>0:
            errors['inuse'] = "Email in use."
        return errors

    def login_validator(self, postData):
        errors={}
        cemail = postData['email']
        user=User.objects.filter(email=cemail)
        print(user)
        # CHECKING EMAIL IN DATABASE
        if not EMAIL_REGEX.match(postData['email']):
            errors['emailformat'] = "Invalid login."
        if len(user)<1:
            errors['emailnot'] = "Invalid login."
        # CHECKING PASSWORD TO BE 8 CHARACTERS, A NUMBER, CAPITAL, LOWERCASE, AND MATCH
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['pwfail'] = "Invalid login."
        return errors

class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors={}
        # CHECKING item AND description NOT EMPTY AND AT LEAST 3 CHARACTERS
        if len(postData['item'])<3 and len(postData['item'])>0:
            errors["item"]= "A wish must consist of at least 3 characters!"
        if len(postData['description'])<3 and len(postData['description'])>0:
            errors["description"]= "A description must be at least 3 characters!"
        # CHECKING item AND description NOT EMPTY
        if len(postData['item']) == 0:
            errors['item'] = 'A wish must be provided!'
        if len(postData['description']) == 0:
            errors['description'] = 'A description must be provided!'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name =models.CharField(max_length=255)
    email =models.CharField(max_length=255)
    password =models.CharField(max_length=255)
    created_at =models.DateField(auto_now_add=True)
    updated_at =models.DateField(auto_now=True)
    objects =UserManager()

class Wish(models.Model):
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    wisher = models.ForeignKey(User, related_name='wishes')
    granted = models.BooleanField(default=False)
    date_granted = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    liker = models.ManyToManyField(User, related_name='wishes_liked')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects =WishManager()