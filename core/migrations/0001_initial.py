# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-27 20:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=12)),
                ('business', models.CharField(max_length=32)),
                ('security_question', models.CharField(choices=[(1, 'Onde você mora?'), (2, 'Qual o seu apelido de colegial?'), (3, 'Qual o nome da(o) sua/seu primera(o) professora/professor?')], default=1, max_length=1)),
                ('security_answer', models.CharField(max_length=64)),
                ('is_visible', models.BooleanField(default=True)),
                ('friends', models.ManyToManyField(blank=True, related_name='_profile_friends_+', to='core.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('until', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='invite',
            name='invited',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convites_received', to='core.Profile'),
        ),
        migrations.AddField(
            model_name='invite',
            name='invitee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='convites_made', to='core.Profile'),
        ),
        migrations.AddField(
            model_name='block',
            name='blocked',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks_received', to='core.Profile'),
        ),
        migrations.AddField(
            model_name='block',
            name='blocker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks_made', to='core.Profile'),
        ),
    ]
