# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0012_auto_20160907_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='profession',
            name='vertical_cover',
            field=models.ImageField(upload_to='cover', verbose_name='\u0412\u0435\u0440\u0442\u0438\u043a\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u0431\u043b\u043e\u0436\u043a\u0430', blank=True),
        ),
    ]
