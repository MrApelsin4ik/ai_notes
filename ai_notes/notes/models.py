from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class Note(models.Model):
    # Заголовок заметки
    title = models.CharField(max_length=500, null=True)

    # Дата создания заметки
    date_created = models.DateTimeField(default=timezone.now)

    # Текст заметки
    text = models.TextField(null=True)


    # Привязка к пользователю
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Порядковый номер заметки для каждого пользователя
    note_number = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            # Определяем порядковый номер заметки для данного пользователя
            last_note = Note.objects.filter(user=self.user).order_by('note_number').last()
            if last_note:
                self.note_number = last_note.note_number + 1
            else:
                self.note_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} (#{self.note_number})'


class NoteFile(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='files')
    upload = models.FileField(upload_to='uploads/')


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email