# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0006_auto_20160826_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professioncomp',
            name='profession',
            field=models.ForeignKey(related_name='competencies', verbose_name='\u041f\u0440\u043e\u0444\u0435\u0441\u0438\u044f', to='plp_eduplanner.Profession'),
        ),
        migrations.AlterField(
            model_name='usercomp',
            name='user',
            field=models.ForeignKey(related_name='competencies', verbose_name='\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL),
        ),
    ]
