from django.db import models
from django.utils.translation import gettext_lazy as _


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=False, verbose_name=_("Description"))
    syllabus = models.FileField(upload_to='syllabuses/', blank=False, null=True, verbose_name=_("Syllabus"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
