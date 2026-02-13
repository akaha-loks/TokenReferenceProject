# main/management/commands/migrate_images_to_cloudinary.py
from django.core.management.base import BaseCommand
from main.models import Post
from django.conf import settings
import cloudinary.uploader
import os
import re


class Command(BaseCommand):
    help = "Upload all local images (cover and instruction images) to Cloudinary"

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()
        for post in posts:
            # ------------------
            # 1. Обложка (cover)
            # ------------------
            if post.image:
                # Если это уже URL Cloudinary, пропускаем
                if str(post.image).startswith("http"):
                    self.stdout.write(self.style.NOTICE(f"Cover already uploaded: {post.title}"))
                else:
                    local_path = os.path.join(settings.MEDIA_ROOT, 'posts', os.path.basename(str(post.image)))
                    if os.path.exists(local_path):
                        result = cloudinary.uploader.upload(local_path, folder="posts")
                        post.image = result['secure_url']
                        post.save()
                        self.stdout.write(self.style.SUCCESS(f"Uploaded cover: {post.title}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Cover not found locally: {post.title}"))

            # ------------------
            # 2. Картинки внутри инструкции (CKEditor)
            # ------------------
            content = post.content
            # Ищем все src="..."
            img_paths = re.findall(r'src="([^"]+)"', content)
            for img_path in img_paths:
                if img_path.startswith(settings.MEDIA_URL):
                    # Получаем реальный путь
                    local_file_path = os.path.join(settings.MEDIA_ROOT, img_path.replace(settings.MEDIA_URL, ''))
                    if os.path.exists(local_file_path):
                        result = cloudinary.uploader.upload(local_file_path, folder="instruction_images")
                        # Заменяем в контенте путь на Cloudinary URL
                        content = content.replace(img_path, result['secure_url'])
                        self.stdout.write(self.style.SUCCESS(f"Uploaded instruction image: {img_path}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Instruction image not found: {img_path}"))

            # Сохраняем обновлённый контент
            post.content = content
            post.save()