from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models.user import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, verbose_name=_("Sender"))
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE,
                                 verbose_name=_("Receiver"))
    content = models.TextField(verbose_name=_("Content"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Timestamp"))

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
