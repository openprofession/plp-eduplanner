# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plp', '0072_merge'),
        ('plp_eduplanner', '0008_auto_20160905_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='courses',
            field=models.ManyToManyField(to='plp.Course', through='plp_eduplanner.Course2Plan'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='profession',
            field=models.ForeignKey(related_name='plans', to='plp_eduplanner.Profession'),
        ),
    ]
