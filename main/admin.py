from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from django.db.models import Q
import re

from .models import Post, Token

admin.site.unregister(Group)


class PostInline(admin.TabularInline):
    model = Post
    extra = 1
    fields = ('title', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'posts_count')
    search_fields = ('name', 'description')
    inlines = [PostInline]

    def description_short(self, obj):
        if obj.description:
            return obj.description[:80] + ('...' if len(obj.description) > 80 else '')
        return '—'
    description_short.short_description = 'Описание'

    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = 'Инструкций'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('preview', 'title', 'token', 'created_at')
    list_filter = ('token', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'preview')
    search_fields = ('title', 'content')

    fieldsets = (
        ('Основная информация', {'fields': ('title', 'token', 'content')}),
        ('Обложка', {'fields': ('image', 'preview')}),
        ('Ссылки и даты', {'fields': ('driver_link', 'created_at')}),
    )

    def preview(self, obj):
        if not obj or not obj.image:
            return '—'

        # Берём URL напрямую из Cloudinary
        url = obj.image.url if hasattr(obj.image, 'url') else str(obj.image)

        return format_html(
            '<img src="{}" style="height:60px; border-radius:6px;" />',
            url
        )

    preview.short_description = 'Обложка'
