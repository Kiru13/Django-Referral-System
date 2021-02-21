import secrets
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from .custom_user_manager import UserManager


class Users(AbstractUser):
    """ Users model with AbstractUser inherited"""
    username = None
    email = models.EmailField(max_length=100, unique=True)
    referral_code = models.CharField(max_length=50)
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


@receiver(signal=post_save, sender=Users)
def create_referral_code(sender, instance, created, **kwargs):
    """ Post save signal to create referral_code with secretes hex token code """
    if created:
        secret_referral_code = secrets.token_hex(3) + str(instance.id)
        instance.referral_code = secret_referral_code
        instance.save()


class Referral(models.Model):
    """ Referral model to track referral logs """
    referrer = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name='referrer')
    referred_to = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, related_name='referred_to')
    to_email = models.EmailField(max_length=100)
    status = models.CharField(max_length=20, default='referred')

    class Meta:
        unique_together = ('referrer', 'to_email')

    def __repr__(self):
        return f'Referrer: {self.referrer}, Referrer To: {self.referred_to}, status:{self.status}'
