# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0003_professionobjective'),
    ]

    operations = [
        migrations.AddField(
            model_name='profession',
            name='sub_title',
            field=models.CharField(max_length=200, verbose_name='\u041f\u043e\u0434 \u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a', blank=True),
        ),
        migrations.AlterField(
            model_name='professionobjective',
            name='profession',
            field=models.ForeignKey(related_name='objectives', verbose_name='\u041f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u044f', to='plp_eduplanner.Profession'),
        ),
    ]
