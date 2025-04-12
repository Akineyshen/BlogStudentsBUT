from django.contrib import admin
from .models import Article, Review, Tag

admin.site.register(Article)
admin.site.register(Review)
admin.site.register(Tag)
