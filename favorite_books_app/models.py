from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name']= "First name must be more than 2 characters"    
        if len(postData['last_name']) < 2:
            errors['last_name']= "Last name must be more than 2 characters"
        if not EMAIL_REGEX.match(postData['email']):  
            errors['email']= "Invalid email address!"
        users_with_email = User.objects.filter(email = postData['email'])
        if len(users_with_email) >= 1:
            errors['duplicate'] = "Email already exists."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Password must match!"
        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title']= "Title required"
        if len(postData['description']) < 5:
            errors['description']= "Description must be at least 5 characters"
        return errors

    def editBook_validator(self, postData):
        errors = {}
        if len(postData['description']) < 10:
            errors['description']= "Description must be at least to 10 characters"
        return errors

class User(models.Model):
    first_name= models.CharField(max_length= 50)
    last_name= models.CharField(max_length=50)
    email= models.CharField(max_length=75)
    password= models.CharField(max_length=50)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects= UserManager()
    #liked_books = a list of books a giver user likes
    #books_uploaded = a list of books uploaded by a given user

class Book(models.Model):
    title= models.CharField(max_length=75)
    description= models.TextField()
    uploaded_by= models.ForeignKey(User, related_name= "books_uploaded", on_delete= models.CASCADE)
    users_who_like= models.ManyToManyField(User, related_name= "liked_books")
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects= BookManager()

# Create your models here.
