# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plp', '0072_merge'),
        ('plp_eduplanner', '0007_auto_20160830_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course2Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course', models.ForeignKey(to='plp.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profession', models.ForeignKey(to='plp_eduplanner.Profession')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='coursecomp',
            name='course',
            field=models.ForeignKey(related_name='competencies', verbose_name='\u041a\u0443\u0440\u0441', to='plp.Course'),
        ),
        migrations.AddField(
            model_name='course2plan',
            name='plan',
            field=models.ForeignKey(to='plp_eduplanner.Plan'),
        ),
    ]
