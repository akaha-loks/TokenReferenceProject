from django.db import models


class Token(models.Model):
    name = models.CharField(
        'Название токена',
        max_length=100
    )
    description = models.TextField(
        'Описание',
        blank=True
    )

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'

    def __str__(self):
        return self.name


class Post(models.Model):
    token = models.ForeignKey(
        Token,
        verbose_name='Токен',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(
        'Заголовок',
        max_length=200
    )
    content = models.TextField(
        'Текст инструкции'
    )
    image = models.ImageField(
        'Обложка',
        upload_to='posts/',
        blank=True,
        null=True
    )
    driver_link = models.URLField(
        'Ссылка на драйвер',
        blank=True
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Инструкция'
        verbose_name_plural = 'Инструкции'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
