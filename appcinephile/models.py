from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pic', default='avatar.jpg')
    bio = models.TextField()

#   def __str__(self): 
#       return self.user.username

class Review(models.Model):
    pen_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=100, blank=True)
    movie_name = models.CharField(max_length=100,blank=True)
    poster = models.ImageField(upload_to='poster_pic', default='default_m.jpg')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)


class Watched_list(models.Model):
    pen_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie_id = models.CharField(max_length=100,blank=True)
    movie_name = models.CharField(max_length=100,blank=True)
    poster = models.ImageField(upload_to='poster_pic', default='default_m.jpg')


#    def __str__(self):
#       return self.user.username

