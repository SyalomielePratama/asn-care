from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class CustomUser(AbstractUser):
    is_pegawai = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set",  # Tambahkan related_name yang unik
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="customuser_set",  # Tambahkan related_name yang unik
        related_query_name="user",
    )

    def __str__(self):
        return self.username
    
@receiver(post_delete, sender=CustomUser)
def delete_related_pegawai(sender, instance, **kwargs):
    if instance.is_pegawai and instance.email:
        from app.models import Pegawai
        try:
            pegawai = Pegawai.objects.get(email=instance.email)
            pegawai.delete()
        except Pegawai.DoesNotExist:
            pass