# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0009_auto_20160905_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='profession',
            name='salary_average',
            field=models.PositiveIntegerField(default=None, null=True, blank=True),
        ),
    ]
