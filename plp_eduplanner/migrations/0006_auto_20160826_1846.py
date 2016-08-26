# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0005_auto_20160826_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competence',
            name='annotation',
            field=models.CharField(max_length=200, verbose_name='\u0410\u043d\u043d\u043e\u0442\u0430\u0446\u0438\u044f', blank=True),
        ),
    ]
