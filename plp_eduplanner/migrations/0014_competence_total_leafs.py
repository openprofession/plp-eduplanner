# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plp_eduplanner', '0013_profession_vertical_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='competence',
            name='total_leafs',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
