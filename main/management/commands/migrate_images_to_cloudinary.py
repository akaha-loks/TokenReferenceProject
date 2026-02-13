# main/management/commands/migrate_images_to_cloudinary.py
from django.core.management.base import BaseCommand
from main.models import Post
import cloudinary.uploader
from django.conf import settings
import os

class Command(BaseCommand):
    help = "Upload all local instruction_images to Cloudinary and update Post.image"

    def handle(self, *args, **kwargs):
        posts = Post.objects.exclude(image='')  # все с картинкой
        for post in posts:
            local_path = os.path.join(settings.MEDIA_ROOT, post.image.name)
            if os.path.exists(local_path):
                # загружаем в Cloudinary
                result = cloudinary.uploader.upload(local_path, folder="instruction_images")
                # обновляем поле image на Cloudinary URL
                post.image = result['secure_url']
                post.save()
                self.stdout.write(self.style.SUCCESS(f"Uploaded {post.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"File not found: {post.title}"))
