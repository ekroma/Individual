from django.contrib import admin
from .models import Post, Tag, PostImage, Like, Answer

admin.site.register([Post, Tag, PostImage, Like, Answer])
