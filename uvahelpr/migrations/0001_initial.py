# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('compensation', models.DecimalField(max_digits=10, decimal_places=2)),
                ('event_time', models.DateTimeField()),
                ('Location', models.CharField(max_length=200)),
                ('time_required', models.DecimalField(max_digits=10, decimal_places=2)),
                ('skills_required', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text_body', models.TextField()),
                ('time_sent', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UvaUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('skills', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='recipient_id',
            field=models.ForeignKey(related_name='recipient', to='uvahelpr.UvaUser'),
        ),
        migrations.AddField(
            model_name='message',
            name='sender_id',
            field=models.ForeignKey(related_name='sender', to='uvahelpr.UvaUser'),
        ),
        migrations.AddField(
            model_name='job',
            name='requester_id',
            field=models.ForeignKey(related_name='requester', to='uvahelpr.UvaUser'),
        ),
        migrations.AddField(
            model_name='job',
            name='servicer_id',
            field=models.ForeignKey(related_name='servicer', to='uvahelpr.UvaUser'),
        ),
    ]
