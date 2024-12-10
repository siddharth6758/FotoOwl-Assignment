from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10}$',
        message='Phone number must be entered in the format: " + 999999999". Up to 10 digits allowed.')

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField("Email ID",unique=True)
    phone = models.CharField("Phone Number",validators=[phone_regex],max_length=10)
    is_librarian = models.BooleanField("Is Librarian",default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        if super().first_name != '' or super().last_name != '':
            name = super().first_name + ' ' + super().last_name
        else:
            name = 'NoName'
        return f"{name} - {super().username}"

    class Meta:
        verbose_name_plural = "User Accounts"