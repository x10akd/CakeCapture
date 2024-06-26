# Generated by Django 5.0.6 on 2024-06-13 05:17

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.TextField(max_length=500)),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_message', models.TextField(max_length=500)),
                ('reply_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('feedback', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='feedbacks.feedback')),
            ],
        ),
    ]
