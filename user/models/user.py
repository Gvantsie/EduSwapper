from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.user_choices.country_choices import COUNTRY_CHOICES


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True, verbose_name=_("Bio"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Birth Date"))
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True,
                                        verbose_name=_("Profile Picture"))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Joined"))

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile',
                                verbose_name=_("User"))
    skills = models.ManyToManyField('Skill', related_name='users_with_skill', verbose_name=_("Skills"))
    interests = models.ManyToManyField('Interest', related_name='users_with_interest', verbose_name=_("Interests"))
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True, null=True, verbose_name=_("Country"))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

