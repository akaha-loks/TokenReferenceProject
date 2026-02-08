from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from django.db.models import Q
import re
from .models import Post

admin.site.unregister(Group)


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

    def get_search_results(self, request, queryset, search_term):
        if search_term:
            search_term = re.sub(r'[^\w\s]', '', search_term)
            words = search_term.split()

            query = Q()
            for word in words:
                word_lower = word.lower()
                query |= Q(title__icontains=word_lower) \
                         | Q(content__icontains=word_lower) \
                         | Q(token__name__icontains=word_lower)

                query |= Q(title__iregex=word) \
                         | Q(content__iregex=word) \
                         | Q(token__name__iregex=word)

            queryset = queryset.filter(query)

        return queryset, False

    def preview(self, obj):
        if not obj or not obj.image:
            return '—'
        return format_html(
            '<img src="{}" style="height:60px; border-radius:6px;" />',
            obj.image.url
        )

    preview.short_description = 'Обложка'
