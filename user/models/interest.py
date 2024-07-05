from django.db import models
from django.utils.translation import gettext_lazy as _


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Interest")
        verbose_name_plural = _("Interests")
