from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Feedback(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField(max_length=500)
    add_time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="feedback", default=None
    )

    def __repr__(self):
        return "Feedback<title = %s, message = %s, add_time = %s>" % (
            self.title,
            self.message,
            self.add_time,
        )


class FeedbackReply(models.Model):
    feedback = models.OneToOneField(
        Feedback, on_delete=models.CASCADE, related_name="reply"
    )
    reply_message = models.TextField(max_length=500)
    reply_time = models.DateTimeField(default=timezone.now)

    def __repr__(self):
        return (
            "FeedbackReply<feedback_id = %s, reply_message = %s, reply_time = %s>"
            % (self.feedback.id, self.reply_message, self.reply_time)
        )
