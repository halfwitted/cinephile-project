from django.contrib import admin
from .models import Profile, Review

# Register your models here.

admin.site.site_url="/cinephileindex"

admin.site.register(Profile)
admin.site.register(Review)
