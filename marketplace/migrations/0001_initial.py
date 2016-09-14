# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('compensation', models.DecimalField(decimal_places=2, max_digits=10)),
                ('event_time', models.DateTimeField()),
                ('Location', models.CharField(max_length=200)),
                ('time_required', models.DecimalField(decimal_places=2, max_digits=10)),
                ('skills_required', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text_body', models.TextField()),
                ('time_sent', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UvaUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('skills', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='recipient_id',
            field=models.ForeignKey(related_name='recipient', to='marketplace.UvaUser'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender_id',
            field=models.ForeignKey(related_name='sender', to='marketplace.UvaUser'),
        ),
        migrations.AddField(
            model_name='job',
            name='requester_id',
            field=models.ForeignKey(related_name='requester', to='marketplace.UvaUser'),
        ),
        migrations.AddField(
            model_name='job',
            name='servicer_id',
            field=models.ForeignKey(related_name='servicer', to='marketplace.UvaUser'),
        ),
    ]
