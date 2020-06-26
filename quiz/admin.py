from django.contrib import admin
from .models import Category, Tag, Quiz, Answer


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Quiz)
admin.site.register(Answer)