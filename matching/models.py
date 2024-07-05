from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models.user import User


class Match(models.Model):
    user1 = models.ForeignKey(User, related_name='matches_as_user1', on_delete=models.CASCADE, verbose_name=_("User 1"))
    user2 = models.ForeignKey(User, related_name='matches_as_user2', on_delete=models.CASCADE, verbose_name=_("User 2"))
    is_accepted_by_user1 = models.BooleanField(default=False, verbose_name=_("Accepted by User 1"))
    is_accepted_by_user2 = models.BooleanField(default=False, verbose_name=_("Accepted by User 2"))

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"

    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")
