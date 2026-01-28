from django.contrib import admin
from .models import Token, Post

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'token', 'created_at')
    list_filter = ('token',)
    search_fields = ('title', 'content')