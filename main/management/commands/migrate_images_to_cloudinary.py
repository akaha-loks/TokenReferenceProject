# main/management/commands/migrate_images_to_cloudinary.py
from django.core.management.base import BaseCommand
from main.models import Post
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
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
                # Проверяем, что это локальный путь, а не URL
                if not str(post.image).startswith("http"):
                    local_path = os.path.join(settings.MEDIA_ROOT, 'posts', os.path.basename(str(post.image)))
                    if os.path.exists(local_path):
                        # Загружаем через default_storage (использует CloudinaryStorage)
                        with open(local_path, "rb") as f:
                            post.image.save(os.path.basename(local_path), ContentFile(f.read()), save=True)
                        self.stdout.write(self.style.SUCCESS(f"Uploaded cover: {post.title}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Cover not found locally: {post.title}"))
                else:
                    self.stdout.write(self.style.NOTICE(f"Cover already uploaded: {post.title}"))

            # ------------------
            # 2. Картинки внутри инструкции (CKEditor)
            # ------------------
            content = post.content
            img_paths = re.findall(r'src="([^"]+)"', content)
            for img_path in img_paths:
                if img_path.startswith(settings.MEDIA_URL):
                    local_file_path = os.path.join(settings.MEDIA_ROOT, img_path.replace(settings.MEDIA_URL, ''))
                    if os.path.exists(local_file_path):
                        # Загружаем на Cloudinary напрямую
                        with open(local_file_path, "rb") as f:
                            file_content = f.read()
                        result = default_storage.save(os.path.basename(local_file_path), ContentFile(file_content))
                        cloud_url = default_storage.url(result)
                        content = content.replace(img_path, cloud_url)
                        self.stdout.write(self.style.SUCCESS(f"Uploaded instruction image: {img_path}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Instruction image not found: {img_path}"))

            # ------------------
            # Сохраняем обновлённый контент
            # ------------------
            post.content = content
            post.save()
