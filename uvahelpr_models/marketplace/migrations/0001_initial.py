# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('skills_required', models.CharField(max_length=1000)),
                ('compensation', models.DecimalField(decimal_places=2, max_digits=10)),
                ('event_time', models.DateTimeField()),
                ('location', models.CharField(max_length=200)),
                ('time_required', models.DecimalField(decimal_places=2, max_digits=10)),
                ('requester_id', models.ForeignKey(related_name='requester', to=settings.AUTH_USER_MODEL)),
                ('servicer_id', models.ForeignKey(related_name='servicer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('text_body', models.TextField()),
                ('time_sent', models.DateTimeField()),
                ('recipient_id', models.ForeignKey(related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender_id', models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('phone_number', models.CharField(validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")], max_length=17, blank=True)),
                ('reputation', models.IntegerField(null=True, blank=True)),
                ('skills', models.CharField(max_length=1000, blank=True)),
                ('user', models.OneToOneField(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
